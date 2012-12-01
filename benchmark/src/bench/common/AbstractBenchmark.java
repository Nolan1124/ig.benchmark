package bench.common;
import java.util.*;
import java.io.*;

public abstract class AbstractBenchmark{
    public final static int DefaultNumberOfThreads = 1;
    public final static int DefaultTransactionSize = 10000;
    public final static IndexType DefaultIndexType = IndexType.Graph;
    public final static int DefaultLimit = 100000;
    public final static String DefaultDatabaseName = "bench";
    public final static String DefaultPropertyFile = "configuration.properties";
    public final static String DefaultServerURI = "http://127.0.0.1:7474/db/data";
    
    protected int numberOfThreads = DefaultNumberOfThreads;
    protected int numberOfVertexIngestThreads = DefaultNumberOfThreads;
    protected int numberOfEdgeIngestThreads = DefaultNumberOfThreads;
    protected int transactionSize = DefaultTransactionSize;
    protected GraphDataSource graphDataSource = null;
    protected Properties properties = null;
    protected boolean useLocalCache = false;
    protected IndexType indexType = DefaultIndexType;

    protected ProfileEvent vertexIngestEvent = new ProfileEvent();
    protected ProfileEvent edgeIngestEvent = new ProfileEvent();
    protected ProfileEvent searchEvent = new ProfileEvent();
    protected ProfileEvent plotEvent = new ProfileEvent();
    protected ProfileEvent readEvent = new ProfileEvent();
    protected ProfileEvent bfsEvent = new ProfileEvent();
    protected ProfileEvent dfsEvent = new ProfileEvent();
    protected ProfileEvent removeEvent = new ProfileEvent();
    
    protected long currentKey = 0;
    protected long sizePerThread = 0;
    protected boolean saveResults = false;

    protected List<List<LongPair>> searchListContainer = new ArrayList<List<LongPair>>();
    protected int limit = DefaultLimit;

    protected String dbName = DefaultDatabaseName;
    protected String propertyFileName = DefaultPropertyFile;


    protected String serverURI = DefaultServerURI;

    public String getServerURI()
    {
        return this.serverURI;
    }

    public void setServerURI(String serverURI)
    {
        this.serverURI = serverURI;
    }
    
    protected void line()
    {
        System.out.println("\t-------------------------------------------------");
    }
    
    public void deleteFileOrDirectory(File file )
    {
        if ( file.exists() )
        {
            if ( file.isDirectory() )
            {
                for ( File child : file.listFiles() )
                {
                    deleteFileOrDirectory( child );
                }
            }
            file.delete();
        }
    }

    
    public List<LongPair> getSearchList(int index)
    {
        return this.searchListContainer.get(index);
    }
        
    public long getCurrentKey()
    {
        return this.currentKey;
    }
    
    public long getSizePerThread()
    {
        return this.sizePerThread;
    }

    public boolean saveResults(){
        return this.saveResults;
    }
    
    public ProfileEvent getVertexIngestEvent(){
        return vertexIngestEvent;
    }

    public ProfileEvent getEdgeIngestEvent(){
        return edgeIngestEvent;
    }

    public ProfileEvent getSearchEvent(){
        return searchEvent;
    }

    public int getLimit(){
        return limit;
    }

    public void setLimit(int limit){
        this.limit = limit;
    }

    public String getDbName(){
        return this.dbName;
    }
     
    public String getPropertyFileName(){
        return this.propertyFileName;
    }

    public void setDbName(String dbName){
        this.dbName = dbName;
    }
    
    public void setPropertyFileName(String propertyFileName){
        this.propertyFileName = propertyFileName;
    }

    
    public String toString(){
        return String.format("Benchmark (%s) {vertex-ingest-threads:%d,edge-ingest-threads:%d,operation-threads:%d,txsize:%d,localcache:%b,indexType:%s}",
                             this.getName(),
                             this.numberOfVertexIngestThreads,
                             this.numberOfEdgeIngestThreads,
                             this.numberOfThreads,
                             this.transactionSize,
                             this.useLocalCache,
                             this.indexType.toString());
        
    }
    
    public static IndexType parseIndexType(final String value){
        IndexType type = AbstractBenchmark.DefaultIndexType;
        if(value != null){
            if(value.equalsIgnoreCase("gr"))
                type = IndexType.Graph;
            else if(value.equalsIgnoreCase("none"))
                type = IndexType.None;
        }
        return type;
    }
    
    public String getName(){
        return this.getClass().getName();
    }

    public void setNumberOfVertexIngestThreads(int value){
        this.numberOfVertexIngestThreads = value;
    }

    public void setNumberOfEdgeIngestThreads(int value){
        this.numberOfEdgeIngestThreads = value;
    }

    public void setTransactionSize(int value){
        this.transactionSize = value;
    }
    
    public void setGraphDataSource(GraphDataSource value){
        this.graphDataSource = value;
    }

    public void setUseLocalCache(boolean value){
        this.useLocalCache = value;
    }

    public void setIndexType(IndexType value){
        this.indexType = value;
    }

    public void setNumberOfThreads(int value){
        this.numberOfThreads = value;
    }
    
    public int getNumberOfVertexIngestThreads(){
        return this.numberOfVertexIngestThreads;
    }
    
    public int getNumberOfEdgeIngestThreads(){
        return this.numberOfEdgeIngestThreads;
    }

    public int getNumberOfThreads(){
        return this.numberOfThreads;
    }
    
    public int getTransactionSize(){
        return this.transactionSize;
    }

    public GraphDataSource getGraphDataSource(){
        return this.graphDataSource;
    }

    public Properties getProperties(){
        return this.properties;
    }

    public boolean getUseLocalCache(){
        return this.useLocalCache;
    }
    
    public IndexType getIndexType(){
        return this.indexType;
    }

    public boolean initialize() throws Exception{
        this.properties = new Properties();
        this.properties.load(new FileReader(this.propertyFileName));
        return true;
    }

    public void flush() throws Exception{
        
    } 
    

    protected long run(String name,ProfileEvent event,int numberOfThreads,AbstractOperationFactory operationFactory) throws Exception{
        String indexType  = this.indexType.toString();
        long databaseSize = this.graphDataSource.getSize(); 
    
        Thread[] threads = new Thread[numberOfThreads];
        HashMap<Thread,AbstractOperation> map = new HashMap<Thread,AbstractOperation>();
        int i;
        String fileName = null;
        this.line();
        System.out.printf("\t - %s -\n",name);
        if(event != null)
            event.start();
        for(i=0;i<numberOfThreads;i++)
        {
            AbstractOperation operation = operationFactory.create(i,this.graphDataSource,this.transactionSize);
            if(fileName == null)
                fileName = operation.getName();
            operation.initialize(this);
            Thread thread = new Thread(operation);
            map.put(thread,operation);
            threads[i] = thread;
            thread.start();
            this.currentKey += sizePerThread;
        }
        long totalCounter = 0;
        for(i=0;i<numberOfThreads;i++)
        {
            Thread thread = threads[i];
            thread.join();
            AbstractOperation operation = map.get(thread);
            long counter = operation.getCounter();
            List<LongPair> result = operation.getResult();
            if(result != null){
                this.searchListContainer.add(result);
            }
            totalCounter += counter;
        }
        if(event != null)
        {
            event.stop(totalCounter);
            this.line();
            System.out.printf("\tTime(ms)       :%d\n",event.getElapsedTime());
            System.out.printf("\tRate(per sec)  :%2.2f\n",event.getRate());
            System.out.printf("\tSize           :%d\n",totalCounter);
            System.out.printf("\tTx size        :%d\n",this.transactionSize);
            System.out.printf("\tThreads        :%d\n",numberOfThreads);
            event.save(fileName,numberOfThreads,this.transactionSize,indexType,databaseSize);       
        }
        this.line();

        return totalCounter;
    }

    protected long ingestVertices(String message,AbstractOperationFactory factory) throws Exception{
        long size = this.graphDataSource.getSize();
        this.sizePerThread  = size/this.numberOfVertexIngestThreads;
        this.sizePerThread += size - (this.sizePerThread * this.numberOfVertexIngestThreads);
        this.currentKey = this.graphDataSource.getOffset();
        return this.run(message,vertexIngestEvent,this.numberOfVertexIngestThreads,factory);
    }

    protected long ingestEdges(String message,AbstractOperationFactory factory) throws Exception{
        return this.run(message,edgeIngestEvent,this.numberOfEdgeIngestThreads,factory);
    }

    protected long search(String message,boolean saveSearchResult,AbstractOperationFactory factory) throws Exception{
        this.saveResults = saveSearchResult;
        if(this.saveResults)
            return this.run(message,null,this.numberOfThreads,factory);
        return this.run(message,searchEvent,this.numberOfThreads,factory);
    }
    
    protected abstract long ingestEdges(boolean pipelined) throws Exception;
    protected abstract long ingestVertices() throws Exception;
        
    public abstract boolean createDB() throws Exception;
    public abstract boolean openDB() throws Exception;
    public abstract boolean closeDB();
    public abstract boolean deleteDB();
    public long standardIngest() throws Exception{
        long vertexCount = this.ingestVertices();
        long edgeCount = 0;
        if(this.graphDataSource.hasEdgeList())
            edgeCount = this.ingestEdges(false);
        return (vertexCount + edgeCount);
    }

    public long acceleratedIngest() throws Exception{
        long vertexCount = this.ingestVertices();
        long edgeCount = 0;
        if(this.graphDataSource.hasEdgeList())
            edgeCount = this.ingestEdges(true);
        return (vertexCount + edgeCount);
    }


    public long acceleratedEdgeIngest() throws Exception{
        long edgeCount = 0;
        if(this.graphDataSource.hasEdgeList())
            edgeCount = this.ingestEdges(true);
        return edgeCount;
    }

    
    public abstract long search(boolean saveSearchResults) throws Exception;
    public abstract long read() throws Exception;
    public abstract long dfsTraverse() throws Exception;
    public abstract long bfsTraverse() throws Exception;
    public abstract long remove() throws Exception;

    public boolean databaseStatus() throws Exception {return false;}
}
