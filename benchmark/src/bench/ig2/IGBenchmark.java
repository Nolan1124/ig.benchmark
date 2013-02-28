package bench.ig2;
import java.util.*;
import java.io.*;
import com.infinitegraph.*;
import com.infinitegraph.indexing.*;
import com.infinitegraph.policies.*;
import bench.common.*;

class IngestVertexFactory implements AbstractOperationFactory
{
    public AbstractOperation create(int i,GraphDataSource graphDataSource,int transactionSize)
    {
        return new IngestVertex(i,graphDataSource,transactionSize);
    }
}

class IngestEdgeFactory implements AbstractOperationFactory
{
    public AbstractOperation create(int i,GraphDataSource graphDataSource,int transactionSize)
    {
        return new IngestEdge(i,graphDataSource,transactionSize);
    }
}

class PipelinedIngestEdgeFactory implements AbstractOperationFactory
{
    public AbstractOperation create(int i,GraphDataSource graphDataSource,int transactionSize)
    {
        return new PipelinedIngestEdge(i,graphDataSource,transactionSize);
    }
}


class FindVertexFactory implements AbstractOperationFactory
{
    public AbstractOperation create(int i,GraphDataSource graphDataSource,int transactionSize)
    {
        return new FindVertex(i,graphDataSource,transactionSize);
    }
}

class ReaderFactory implements AbstractOperationFactory
{
    public AbstractOperation create(int i,GraphDataSource graphDataSource,int transactionSize)
    {
        return new Reader(i,graphDataSource,transactionSize);
    }
}

class BFSTraversalFactory implements AbstractOperationFactory
{
    public AbstractOperation create(int i,GraphDataSource graphDataSource,int transactionSize)
    {
        return new BFSTraversal(i,graphDataSource,transactionSize);
    }
}

class DFSTraversalFactory implements AbstractOperationFactory
{
    public AbstractOperation create(int i,GraphDataSource graphDataSource,int transactionSize)
    {
        return new DFSTraversal(i,graphDataSource,transactionSize);
    }
}

class RemoveFactory implements AbstractOperationFactory
{
    public AbstractOperation create(int i,GraphDataSource graphDataSource,int transactionSize)
    {
        return new Remove(i,graphDataSource,transactionSize);
    }
}

public class IGBenchmark extends bench.common.AbstractBenchmark
{
    private GraphDatabase graphDB   = null;
    private VertexFactory vertexFactory = null; 

    public VertexFactory getVertexFactory()
    {
        return this.vertexFactory;
    }

    public GraphDatabase getGraphDB()
    {
        return this.graphDB;
    }
    
    public boolean initialize() throws Exception
    {
        boolean status = false;
        if(super.initialize() == true)
        {
            if(this.indexType == bench.common.IndexType.None)
            {
                vertexFactory = new VertexFactory(this.useLocalCache);   
                status = true;
            }
            else if(this.indexType == bench.common.IndexType.Graph)
            {
                vertexFactory = new GraphVertexFactory(this.useLocalCache);
                status = true;
            }
            else
            {
                vertexFactory = new VertexFactory(this.useLocalCache); 
            }
            if(vertexFactory != null)
                vertexFactory.initialize();
        }
        return status;
    }

    public void flush() throws Exception
    {
        this.vertexFactory.flush();
    }
    
    private Transaction createWriteTransaction()
    {
        return this.graphDB.beginTransaction(AccessMode.READ_WRITE);
    }
    
    public boolean createDB() throws Exception
    {
        boolean status = true;
        if(this.verboseLevel >= 2)
            System.out.println("\t\t> Create DB ...");
        try
        {
            this.deleteDB();
            GraphFactory.create(this.getDbName(),this.getPropertyFileName());
            Transaction transaction = null;
            try
            {
                this.graphDB = GraphFactory.open(this.getDbName(),this.getPropertyFileName());
                transaction = this.createWriteTransaction();
                this.vertexFactory.createIndex(this.graphDB);
                transaction.commit();
            }
            catch(IndexException ie)
            {
                ie.printStackTrace();
                status = false;
            }
            finally
            {
                if(transaction != null)
                    transaction.complete();
            }
        }
        catch (ConfigurationException ce)
        {
            ce.printStackTrace();
            status = false;
        }
        if(this.verboseLevel >= 2)
            System.out.println("\t\t< Create DB ...");
        return status;
    }

    public boolean deleteDB()
    {
        boolean status = true;
        if(this.verboseLevel >= 2)
            System.out.println("\t\t> Delete DB ...");
        try
        {
            GraphFactory.delete(this.getDbName(),this.getPropertyFileName());
        }
        catch (StorageException se){
            status = false;
        }
        catch (ConfigurationException ce)
        {
            System.out.println(ce.getMessage());
            status = false;
        }
        if(this.verboseLevel >= 2)
            System.out.println("\t\t< Delete DB ...");
        return status;
    }
    
    
    public boolean openDB() throws Exception{
        try{
            this.graphDB = GraphFactory.open(this.getDbName(),this.getPropertyFileName());
            Transaction transaction = this.createWriteTransaction();
            this.vertexFactory.initializeIndex(this.graphDB);
            transaction.commit();
        }
        catch(Exception e){
            e.printStackTrace();
            return false;
        }
        return true;
    }
    
    public boolean closeDB(){
        if(this.graphDB != null)
            this.graphDB.close();
        return true;
    }

    protected long ingestVertices() throws Exception{
        return super.ingestVertices("Ingest Vertices",new IngestVertexFactory());
    }

    protected long ingestEdges(boolean pipelined) throws Exception
    {
        if(pipelined)
            return super.ingestEdges("Ingest Edges (Pipelined) ",new PipelinedIngestEdgeFactory());
        return this.ingestEdges("Ingest Edges (Standard)",new IngestEdgeFactory());
     }

    
    public long search(boolean saveSearchResults) throws Exception
    {
        return super.search("Search Vertices",saveSearchResults,new FindVertexFactory());
    }
        
    public long read() throws Exception
    {
        return this.run("Read Graph",readEvent,this.numberOfThreads,new ReaderFactory());
    }

    public long dfsTraverse() throws Exception
    {
        //this.search(true);
        return this.run("DFS Traversal",dfsEvent,this.numberOfThreads,new DFSTraversalFactory());
    }
    
    public long bfsTraverse() throws Exception
    {
        //this.search(true);
        return this.run("BFS Traversal",bfsEvent,this.numberOfThreads,new BFSTraversalFactory());
    }
    

    public long remove() throws Exception
    {
        this.saveResults = true;
        this.searchListContainer.clear();
        this.run("Read Graph vertices for use in removal",null,1,new ReaderFactory());
        List<LongPair> removeList = this.searchListContainer.get(0);
        int sizePerThread = removeList.size()/this.numberOfThreads;
        this.searchListContainer.clear();
        for(int i=0;i<this.numberOfThreads;i++){
            int start = sizePerThread*i;
            int end   = start + sizePerThread;
            this.searchListContainer.add(removeList.subList(start,end));
        }
        return this.run("Remove Vertices",removeEvent,this.numberOfThreads,new RemoveFactory());
    }

}

