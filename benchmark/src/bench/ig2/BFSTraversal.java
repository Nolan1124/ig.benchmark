package bench.ig2;
import com.infinitegraph.*;
import com.infinitegraph.navigation.*;
import java.util.*;
import bench.common.*;

public class BFSTraversal extends Traversal{
    public BFSTraversal(int id,bench.common.GraphDataSource dataSource,int operationsPerTransaction){
        super(id,dataSource,operationsPerTransaction);
    }

    public Guide getGuide(){
        return Guide.SIMPLE_BREADTH_FIRST;
    }
    
}
