package bench.common;

public class LongPair
{
    private long first  = -1;
    private long second = -1;

    public LongPair()
    {
    }
    
    public LongPair(long a,long b)
    {
        this.set(a,b);
    }
    
    public void set(long a,long b)
    {
        this.first = a;
        this.second = b;
    }

    public long getFirst()
    {
        return this.first;
    }

    public long getSecond()
    {
        return this.second;
    }
}
