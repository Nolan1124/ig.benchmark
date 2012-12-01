package bench.ig3;
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

    public BenchResultsHandler()
    {
    }
    
    public void handleResultPath(Path result, Navigator navigator)
    {
        for(Hop h : result)
        {
            if(h.hasEdge())
                counter += 1;
        }
    }

    public void	handleNavigatorFinished(Navigator navigator)
    {
        
    }
}

class ResultQualifier implements Qualifier
{
    private long counter = 0;
    private long id;
    public ResultQualifier(long id)
    {
        this.id = id;
    }
    
    public long getCounter()
    {
        return this.counter;
    }
    
    public boolean qualify(Path currentPath)
    {
        if(currentPath.getFinalHop().getVertex().getId() == this.id)
        {
            this.counter++;
            return true;
        }
        return false;
    }
}

class PathQualifier implements Qualifier
{
    private long counter = 0;
    private long limit;
    
    public PathQualifier(long limit)
    {
        this.limit = limit;
    }

    public long getCounter()
    {
        return this.counter;
    }
    
    public boolean qualify(Path currentPath)
    {
        this.counter += 1;
        if(this.limit < this.counter)
        {
            return false;
        }
        return true;
    }
}



public abstract class Traversal extends IGOperation
{
    private List<LongPair> searchList = null;
    private int limit;
    
    public Traversal(int id,bench.common.GraphDataSource dataSource,int operationsPerTransaction)
    {
        super(id,dataSource,operationsPerTransaction);
    }

    public void initialize(bench.common.AbstractBenchmark benchmark) throws Exception
    {
        super.initialize(benchmark);
        searchList = benchmark.getSearchList(this.id);
        this.limit = benchmark.getLimit();
    }

    public abstract Guide getGuide();
    
    public void operate() throws Exception
    {
        this.counter = 0;
        if(this.searchList != null){
            for(bench.common.LongPair vertexPair:searchList){
                this.createReadTransaction();
                long firstId  = vertexPair.getFirst();
                long secondId = vertexPair.getSecond();
                bench.ig3.Vertex first = (bench.ig3.Vertex)this.graphDB.getVertex(firstId);
                BenchResultsHandler resultPrinter = new BenchResultsHandler();
                ResultQualifier qualifier = new ResultQualifier(secondId);
                PathQualifier pathQualifier = new PathQualifier(this.limit);
                Navigator navigator = first.navigate(this.getGuide(),pathQualifier, qualifier, resultPrinter);
                navigator.start();
                navigator.stop();
                this.counter += pathQualifier.getCounter();
                this.commitTransaction();
            }
        }
    }
    
    
}
