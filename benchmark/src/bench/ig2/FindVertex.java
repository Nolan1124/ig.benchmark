package bench.ig2;
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
            List<Long> searchList = this.dataSource.getNextSearchList(this.operationsPerTransaction);
            int size = searchList.size();
            if(size > 0)
            {
                this.createReadTransaction();
                for(Long vertexID:searchList)
                {
                    Vertex vertex = vertexFactory.findObject(this.graphDB,indexManager,vertexID);
                    System.out.printf("Find V(%d) - >(%d)\n",vertexID,vertex.getId());
                    this.counter += 1;
                    if(vertex != null)
                        elementsFound++;
                }
                this.commitTransaction();
                if(this.verboseLevel >= 2)
                    System.out.printf("\t[%d] %s (%d/%d) \n",this.id,this.getName(),elementsFound,counter);
            }
            if(size < this.operationsPerTransaction)
            {
                done = true;
            }
        }

    }
}
