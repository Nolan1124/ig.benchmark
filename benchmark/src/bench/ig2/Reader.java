package bench.ig2;
import com.infinitegraph.*;
import java.util.*;
import bench.common.*;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.util.Random;

public class Reader extends IGOperation
{
    private List<LongPair> results = null;
    private int limit;
    public Reader(int id,bench.common.GraphDataSource dataSource,int operationsPerTransaction)
    {
        super(id,dataSource,operationsPerTransaction);
    }

    public void initialize(bench.common.AbstractBenchmark benchmark) throws Exception
    {
        super.initialize(benchmark);
        if(benchmark.saveResults() == true)
        {
            results = new ArrayList<LongPair>();
        }
        this.limit = benchmark.getLimit();
    }

    public List<LongPair> getResult()
    {
        return this.results;
    }
    
    public void operate() throws Exception
    {
        this.createReadTransaction();
        Iterator<com.infinitegraph.Vertex> i = this.graphDB.getVertices().iterator();
        boolean read = i.hasNext();
        this.counter = 0;
        while(read){
            Vertex v = (Vertex)i.next();
            long value = v.getKey();
            Iterable<VertexHandle> neighbors = v.getNeighbors();
            if(this.results != null){
                this.results.add(new LongPair(v.getId(),0));
            }
            else{
                for(VertexHandle n:neighbors){
                    Vertex nv = (Vertex)n.getVertex();
                    long nValue = nv.getKey();
                    this.counter++;
                }
            }
            this.counter += 1;
            read = (this.counter < this.limit) && (i.hasNext());
        }
        this.commitTransaction();
    }
}
