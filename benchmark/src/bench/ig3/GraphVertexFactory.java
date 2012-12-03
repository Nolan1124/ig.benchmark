package bench.ig3;

import com.infinitegraph.indexing.IndexManager;
import com.infinitegraph.GraphDatabase;
import com.infinitegraph.Query;

public class GraphVertexFactory extends VertexFactory
{
    
    public GraphVertexFactory(boolean useLocalMap)
    {
        super(useLocalMap);
    }

    public Object createIndex(GraphDatabase graphDB) throws Exception
    {
        IndexManager.addGraphIndex("vertexGraphIndex", bench.ig3.Vertex.class.getName(), new String[] {"key"}, true);
        return null;
    }

    public Object initializeIndex(GraphDatabase graphDB) throws Exception
    {
        return null;
    }
    
    public synchronized bench.ig3.Vertex findObject(GraphDatabase graphDB,Object object,long value) throws Exception
    {
        Query<bench.ig3.Vertex> query = graphDB.createQuery(bench.ig3.Vertex.class.getName(),String.format("key == %d",value));
        return query.getSingleResult();
    }
    
}
