package bench.ig2;

import com.infinitegraph.GraphDatabase;
import com.infinitegraph.indexing.*;
import java.util.*;
import bench.common.*;

public class VertexFactory extends AbstractVertexFactory{
    public VertexFactory(boolean useLocalMap){
        super(useLocalMap);
    }

    public Vertex createVertex(GraphDatabase graphDB,Object indexObject,long value) throws Exception{
        Vertex vertex = this.createVertexObject(graphDB,indexObject,value);
        super.put(value,vertex.getId());
        return vertex;
    }

    public synchronized void removeVertex(GraphDatabase graphDB,Object indexObject,Vertex vertex) throws Exception{
        super.remove(vertex.getId());
        this.removeVertexObject(graphDB,indexObject,vertex);
    }
    
    public Vertex createVertexObject(GraphDatabase graphDB,Object indexObject,long value) throws Exception{
        Vertex vertex = new Vertex(value);
        graphDB.addVertex(vertex);
        return vertex;
    }
    
    public void removeVertexObject(GraphDatabase graphDB,Object indexObject,Vertex vertex) throws Exception{
        graphDB.removeVertex(vertex);
    }

    public Object createIndex(GraphDatabase graphDB) throws Exception {return null;}
    public Object initializeIndex(GraphDatabase graphDB) throws Exception {return null;}
    public Vertex findObject(GraphDatabase graphDB,Object object,long value) throws Exception {return null;}

    public void startWrite() throws Exception {}
    public void commitWrite() throws Exception {}
}
