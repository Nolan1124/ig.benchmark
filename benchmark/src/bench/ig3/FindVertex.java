package bench.ig3;
import com.infinitegraph.*;
import java.util.*;
import bench.common.*;

public class FindVertex extends IGOperation
{
    private List<LongPair> results = null;
    
    public FindVertex(int id,bench.common.GraphDataSource dataSource,int operationsPerTransaction)
    {
        super(id,dataSource,operationsPerTransaction);
    }

    public List<LongPair> getResult()
    {
        return this.results;
    }

     public void initialize(bench.common.AbstractBenchmark benchmark) throws Exception
    {
        super.initialize(benchmark);
        if(benchmark.saveResults() == true)
        {
            results = new ArrayList<LongPair>();
        }
     }
        
    public void operate() throws Exception
    {
        this.counter = 0;
        boolean done = false;
        long elementsFound = 0;
        while(!done)
        {
            List<LongPair> edgePairList = this.dataSource.getNextSearchPair(this.operationsPerTransaction);
            int size = edgePairList.size();
            if(size > 0)
            {
                this.createReadTransaction();
                for(LongPair edgePair:edgePairList)
                {
                    long first = edgePair.getFirst();
                    long second = edgePair.getSecond();
                    Vertex firstVertex = vertexFactory.findObject(this.graphDB,indexManager,first);
                    Vertex secondVertex = vertexFactory.findObject(this.graphDB,indexManager,second);
                    this.counter += 2;
                    if(firstVertex != null)
                        elementsFound++;
                    if(secondVertex != null)
                        elementsFound++;
                    
                    if(this.results != null)
                    {
                        if(firstVertex != null)
                        {
                            if(secondVertex != null)
                            {
                                this.results.add(new LongPair(firstVertex.getId(),secondVertex.getId()));
                            }
                        }
                    }
                }
                this.commitTransaction();
                System.out.printf("\t[%d] %s (%d/%d) \n",this.id,this.getName(),elementsFound,counter);
            }
            if(size < this.operationsPerTransaction)
            {
                done = true;
            }
        }

    }
}
