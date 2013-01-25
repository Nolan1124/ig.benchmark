package bench.ig2;
import com.infinitegraph.*;
import com.infinitegraph.policies.*;
import java.util.*;
import bench.common.*;

public class PipelinedIngestEdge extends IngestEdge
{
    public PipelinedIngestEdge(int id,bench.common.GraphDataSource dataSource,int operationsPerTransaction)
    {
        super(id,dataSource,operationsPerTransaction);
    }

    protected void createEdgeIngestTransaction() throws Exception
    {
        this.createWriteTransaction(true);
    }
    
}
