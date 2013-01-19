package bench.ig2;

import com.infinitegraph.indexing.*;
import com.infinitegraph.GraphDatabase;

public class GraphVertexFactory extends VertexFactory
{
    public GraphVertexFactory(boolean useLocalMap)
    {
        super(useLocalMap);
    }
    
    public Object createIndex(GraphDatabase graphDB) throws Exception
    {
        return IndexManager.<bench.ig2.Vertex>createGraphIndex("vertexGraphIndex",Vertex.class.getName(),"value");
    }

    public Object initializeIndex(GraphDatabase graphDB) throws Exception
    {
        return IndexManager.<bench.ig2.Vertex>getGraphIndex(Vertex.class.getName(),"value");
    }

    //public synchronized bench.ig2.Vertex findObject(GraphDatabase graphDB,Object object,long value) throws Exception
    public bench.ig2.Vertex findObject(GraphDatabase graphDB,Object object,long value) throws Exception
    {
        Vertex vertex = null;
        try
        {
            vertex = ((GraphIndex<bench.ig2.Vertex>)object).getSingleResult("value",(Long)value); 
        }
        catch(Throwable t)
        {
            System.out.printf("[IG2] Exception (%s) when searching for (value=%d)\n",t.getMessage(),value);
            vertex = null;
        }
        return vertex;
    }
}
