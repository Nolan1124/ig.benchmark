package bench.ig3;
import com.infinitegraph.*;
import java.util.*;
import bench.common.*;

public class IngestEdge extends IGOperation
{
    protected boolean useLocalCache;
    public IngestEdge(int id,bench.common.GraphDataSource dataSource,int operationsPerTransaction)
    {
        super(id,dataSource,operationsPerTransaction);
    }

    public void initialize(bench.common.AbstractBenchmark benchmark) throws Exception
    {
        super.initialize(benchmark);
        this.useLocalCache = benchmark.getUseLocalCache();
    }
    
    public void operate() throws Exception
    {
        if(this.useLocalCache)
            this.buildUsingMap();
        else
            this.build();
    }

    protected void createEdgeIngestTransaction() throws Exception
    {
        this.createWriteTransaction(false);
    }
    
    private void buildUsingMap() throws Exception
    {
        this.counter = 0;
        boolean done = false;
        long edgesCreated = 0;
        long sameCounter = 0;
        while(!done)
        {
            List<LongPair> edgePairList = this.dataSource.getNextEdgePair(this.operationsPerTransaction);
            int size = edgePairList.size();
            edgesCreated = 0;
            if(size > 0)
            {
                this.createEdgeIngestTransaction();
                for(LongPair edgePair:edgePairList){
                    long first = edgePair.getFirst();
                    long second = edgePair.getSecond();
                    long firstID = vertexFactory.getVertexId(first);
                    long secondID = vertexFactory.getVertexId(second);
                    if((firstID != -1) && (secondID != -1))
                    {
                        Edge edge = new Edge();
                        this.graphDB.addEdge(edge,firstID,secondID,EdgeKind.OUTGOING,(short)0);
                        edgesCreated++;
                    }
                    if(first == second)
                        sameCounter += 1;
                }
                counter += edgesCreated;
                this.commitTransaction();
            }
            if(size < this.operationsPerTransaction)
            {
                done = true;
            }
        }
    }
    
    private void build() throws Exception
    {
        this.counter = 0;
        boolean done = false;
        long edgesCreated = 0;
        while(!done)
        {
            List<LongPair> edgePairList = this.dataSource.getNextEdgePair(this.operationsPerTransaction);
            int size = edgePairList.size();
            edgesCreated = 0;
            if(size > 0)
            {
                this.createEdgeIngestTransaction();
                for(LongPair edgePair:edgePairList)
                {
                    long first = edgePair.getFirst();
                    long second = edgePair.getSecond();
                    Vertex firstVertex = vertexFactory.findObject(this.graphDB,this.indexManager,first);
                    Vertex secondVertex = vertexFactory.findObject(this.graphDB,this.indexManager,second);
                    
                    if((firstVertex != null) && (secondVertex != null))
                    {
                        Edge edge = new Edge();
                        this.graphDB.addEdge(edge,firstVertex.getId(),secondVertex.getId(),EdgeKind.OUTGOING,(short)0);
                        edgesCreated++;
                    }
                    else
                    {
                        System.out.printf("Unable to match (%d,%d)\n",first,second);
                    }
                }
                counter += edgesCreated;
                this.commitTransaction();
            }
            if(size < this.operationsPerTransaction)
            {
                done = true;
            }
        }
    }    
}
