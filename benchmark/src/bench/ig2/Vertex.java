package bench.ig2;

import com.infinitegraph.BaseVertex;
public class Vertex extends BaseVertex
{
    private long key;
    public Vertex(long value)
    {
        setKey(value);
    }

    public void setKey(long value)
    {
        markModified();
        this.key = value;
    }

    public long getKey()
    {
        fetch();
        return this.key;
    }

}
