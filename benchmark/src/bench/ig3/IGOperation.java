package bench.ig3;
import com.infinitegraph.*;
import com.infinitegraph.policies.*;

public abstract class IGOperation extends bench.common.AbstractOperation
{
    protected GraphDatabase graphDB;
    protected PolicyChain edgePolicy = new PolicyChain(new EdgePipeliningPolicy());
    protected VertexFactory vertexFactory = null;
    protected Object indexManager = null;
    protected Transaction currentTransaction = null;
    protected int verboseLevel = 1;
    
    public IGOperation(int id,bench.common.GraphDataSource dataSource,int operationsPerTransaction)
    {
        super(id,dataSource,operationsPerTransaction);
    }

    public void initialize(bench.common.AbstractBenchmark benchmark) throws Exception
    {
        IGBenchmark igBenchmark = (IGBenchmark)benchmark;
        this.graphDB = igBenchmark.getGraphDB();
        vertexFactory = igBenchmark.getVertexFactory();
        this.verboseLevel = benchmark.getVerboseLevel();
    }

    protected void createReadTransaction() throws Exception
    {
        currentTransaction = this.graphDB.beginTransaction(AccessMode.READ);
        indexManager = this.vertexFactory.initializeIndex(this.graphDB);
    }

    protected void createWriteTransaction(boolean pipelined) throws Exception
    {
        if(pipelined)
            currentTransaction = this.graphDB.beginTransaction(AccessMode.READ_WRITE,this.edgePolicy);
        else
            currentTransaction = this.graphDB.beginTransaction(AccessMode.READ_WRITE);
        indexManager = this.vertexFactory.initializeIndex(this.graphDB);
        this.vertexFactory.startWrite();
    }
    
    protected void commitTransaction() throws Exception
    {
        if(this.verboseLevel >= 3)
            System.out.printf("\t\t[%d] %s Tx Commit [%d]\n",id,this.getName(),counter);
        if(this.currentTransaction != null)
        {
//Will fail...
            this.vertexFactory.commitWrite();
            this.currentTransaction.commit();
            this.currentTransaction.complete();
            this.currentTransaction = null;
            indexManager = null;
        }
    }
    
}
