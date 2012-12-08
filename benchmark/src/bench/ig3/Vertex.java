package bench.ig3;

import com.infinitegraph.BaseVertex;
public class Vertex extends BaseVertex
{
    private long value;
    public Vertex(long value)
    {
        setValue(value);
    }

    public void setValue(long value)
    {
        markModified();
        this.value = value;
    }

    public long getValue()
    {
        fetch();
        return this.value;
    }

}
