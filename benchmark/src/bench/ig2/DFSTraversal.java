package bench.ig2;
import com.infinitegraph.*;
import com.infinitegraph.navigation.*;
import java.util.*;
import bench.common.*;

public class DFSTraversal extends Traversal{
    public DFSTraversal(int id,bench.common.GraphDataSource dataSource,int operationsPerTransaction){
        super(id,dataSource,operationsPerTransaction);
    }

    public Guide getGuide(){
        return Guide.SIMPLE_DEPTH_FIRST;
    }    
}
