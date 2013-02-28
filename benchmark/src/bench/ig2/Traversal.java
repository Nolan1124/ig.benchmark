package bench.ig2;
import com.infinitegraph.*;
import com.infinitegraph.navigation.*;
import java.util.*;
import bench.common.*;

class BenchResultsHandler implements NavigationResultHandler
{
    private long counter = 0;
    public long getCounter()
    {
        return this.counter;
    }
    public BenchResultsHandler(){}
    public void handleResultPath(Path result, Navigator navigator)
    {
        for(Hop h : result)
        {
            if(h.hasEdge())
                counter += 1;
        }
    }

    public void handleNavigatorFinished(Navigator navigator)
    {
    }
}

class ResultQualifier implements Qualifier{
    private long counter = 0;
    private long id;
    public ResultQualifier(long id){
        this.id = id;
    }
    
    public long getCounter(){
        return this.counter;
    }
    
    public boolean qualify(Path currentPath)
    {
        boolean status = (currentPath.getFinalHop().getVertex().getId() == this.id);
        if(status)
        {
            System.out.printf("RESULT Q status=%d\n",status);
            this.counter++;
            return true;
        }
        return false;
    }
}

class PathQualifier implements Qualifier{
    private long counter = 0;
    private long limit;
    
    public PathQualifier(long limit)
    {
        this.limit = limit;
    }

    public long getCounter(){
        return this.counter;
    }
    
    public boolean qualify(Path currentPath){
        this.counter += 1;
        /*
        if((counter % 100) == 0)
        {
            bench.ig2.Vertex v = (bench.ig2.Vertex)(currentPath.getFinalHop().getVertex());
            System.out.printf("(%d) [%d] \n",counter,v.getValue());
        }
        */
        return true;
    }
}



public abstract class Traversal extends IGOperation{
    private List<LongPair> searchList = null;
    private int limit;
    
    public Traversal(int id,bench.common.GraphDataSource dataSource,int operationsPerTransaction){
        super(id,dataSource,operationsPerTransaction);
    }

    public void initialize(bench.common.AbstractBenchmark benchmark) throws Exception{
        super.initialize(benchmark);
        this.limit = benchmark.getLimit();
    }

    public abstract Guide getGuide();
    
    public void operate() throws Exception{
        this.counter = 0;
        List<LongPair> vPairList = this.dataSource.getNextEdgePair(1);
        if(vPairList != null){
            for(bench.common.LongPair vertexPair:vPairList){
                this.createReadTransaction();
                long first  = vertexPair.getFirst();
                com.infinitegraph.Vertex firstVertex = vertexFactory.findObject(this.graphDB,this.indexManager,first);
                if(firstVertex == null)
                {
                    long id = vertexFactory.getVertexId(first);
                    firstVertex = this.graphDB.getVertex(id);
                }
                System.out.printf("Start from %d [%s] oid:%d\n",first,firstVertex,firstVertex.getId());
                BenchResultsHandler resultPrinter = new BenchResultsHandler();
                // ResultQualifier qualifier = new ResultQualifier(secondVertex.getId());
                PathQualifier pathQualifier = new PathQualifier(this.limit);
                Qualifier qualifier = Qualifier.FOREVER;
                Navigator navigator = firstVertex.navigate(this.getGuide(),pathQualifier, qualifier, resultPrinter);
                navigator.start();
                navigator.stop();
                this.counter += pathQualifier.getCounter();
                this.commitTransaction();
            }
        }
    }
    
}
