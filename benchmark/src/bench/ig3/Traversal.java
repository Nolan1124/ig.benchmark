package bench.ig3;
import com.infinitegraph.*;
import com.infinitegraph.navigation.*;
import java.util.*;
import bench.common.*;
import com.infinitegraph.policies.PolicyChain;
import com.infinitegraph.navigation.policies.*;
import com.infinitegraph.navigation.policies.MaximumResultCountPolicy;


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
        boolean status = (currentPath.getFinalHop().getVertexHandle().getId() == this.id);       
        if(status)
        {
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
            bench.ig3.Vertex v = (bench.ig3.Vertex)(currentPath.getFinalHop().getVertex());
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
        PolicyChain policies = new PolicyChain(new MaximumPathDepthPolicy(10));
        MaximumResultCountPolicy p = new MaximumResultCountPolicy(10000000);
        policies.addPolicy(p);
        
        this.counter = 0;
        List<LongPair> vPairList = this.dataSource.getNextEdgePair(this.operationsPerTransaction);
        if(vPairList != null){
            for(bench.common.LongPair vertexPair:vPairList){
                this.createReadTransaction();
                GraphView view = null;//new GraphView();
                long first  = vertexPair.getFirst();
                com.infinitegraph.Vertex firstVertex = vertexFactory.findObject(this.graphDB,this.indexManager,first);
                if(firstVertex == null)
                {
                    long id = vertexFactory.getVertexId(first);
                    firstVertex = this.graphDB.getVertex(id);
                }
                System.out.printf("Start from %d [%s] oid:%d\n",first,firstVertex,firstVertex.getId());
              
                BenchResultsHandler resultPrinter = new BenchResultsHandler();
                PathQualifier pathQualifier = new PathQualifier(this.limit);
                Qualifier qualifier = Qualifier.FOREVER;
                Navigator navigator = firstVertex.navigate(view,this.getGuide(),pathQualifier, qualifier,policies, resultPrinter);
                //Navigator navigator = firstVertex.navigate(view,this.getGuide(),Qualifier.FOREVER, Qualifier.ANY,policies, resultPrinter);
                navigator.start();
                navigator.stop();
                this.counter += pathQualifier.getCounter();
                this.commitTransaction();
            }
        }
    }
    
    
}
