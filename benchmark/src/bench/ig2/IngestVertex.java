package bench.ig2;
import com.infinitegraph.*;
import java.util.*;

public class IngestVertex extends IGOperation{
    protected long startKey;
    protected long size;
        
    public IngestVertex(int id,bench.common.GraphDataSource dataSource,int operationsPerTransaction)
    {
        super(id,dataSource,operationsPerTransaction);
    }

    public void initialize(bench.common.AbstractBenchmark benchmark) throws Exception
    {
        super.initialize(benchmark);
        this.startKey = benchmark.getCurrentKey();
        this.size     = benchmark.getSizePerThread();
    }
    
    public void operate() throws Exception
    {
        this.counter = 0;
        long key = this.startKey;
        this.createWriteTransaction(false);
        if(this.verboseLevel >= 2)
            System.out.printf("[%d] Start ingest vertices at %d\n",this.id,key);
        while(counter < size){
            Vertex vertex = vertexFactory.createVertex(this.graphDB,this.indexManager,key);
            key += 1;
            counter += 1;
            if((counter % operationsPerTransaction) == 0){
                this.commitTransaction();
                if(counter < size)
                    this.createWriteTransaction(false);
            }
        }
        this.commitTransaction();
        if(this.verboseLevel >= 2)
            System.out.printf("[%d] End ingest vertices at %d\n",this.id,key-1);
    }
}
