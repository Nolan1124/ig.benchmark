package bench.ig2;
import com.infinitegraph.*;
import java.util.*;
import bench.common.*;

public class Remove extends IGOperation
{
    private int limit;
    private List<LongPair> searchList = null;
    
    public Remove(int id,bench.common.GraphDataSource dataSource,int operationsPerTransaction)
    {
        super(id,dataSource,operationsPerTransaction);
    }

    public void initialize(bench.common.AbstractBenchmark benchmark) throws Exception
    {
        super.initialize(benchmark);
        this.limit = benchmark.getLimit();
        this.searchList = benchmark.getSearchList(this.id);
    }
    
    public void operate() throws Exception{
        if(this.searchList != null){
            this.createWriteTransaction(false);
            for(bench.common.LongPair vertexPair:searchList){
                long vertexId  = vertexPair.getFirst();
                Vertex v = (Vertex)this.graphDB.getVertex(vertexId);
                if(v != null){
                    Iterable<EdgeHandle> edgeHandle = v.getEdges();
                    for(EdgeHandle e:edgeHandle){
                        Edge edge = (Edge)e.getEdge();
                        if(edge != null){
                            this.graphDB.removeEdge(e.getEdge());
                            this.counter++;
                        }
                    }
                    this.vertexFactory.removeVertex(this.graphDB,this.indexManager,v);
                    this.counter++;
                }
            }
            this.commitTransaction();
        }
    }
}
