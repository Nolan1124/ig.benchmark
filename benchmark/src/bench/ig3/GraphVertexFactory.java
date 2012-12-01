package bench.ig3;

import com.infinitegraph.indexing.*;
import com.infinitegraph.GraphDatabase;

public class GraphVertexFactory extends VertexFactory
{
    public GraphVertexFactory(boolean useLocalMap){
        super(useLocalMap);
    }


    /*
    public Object createIndex(GraphDatabase graphDB) throws Exception{
        return IndexManager.<Vertex>createGraphIndex(Vertex.class.getName(),"key");
    }

    public Object initializeIndex(GraphDatabase graphDB) throws Exception{
        return IndexManager.<Vertex>getGraphIndex(Vertex.class.getName(),"key");
    }

    public synchronized Vertex findObject(GraphDatabase graphDB,Object object,long value) throws Exception{
        return ((GraphIndex<Vertex>)object).getSingleResult(value);
    }

    */
    
}
