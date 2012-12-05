package bench.common;
import java.util.*;

public abstract class AbstractOperation implements Runnable
{
    protected int id;
    protected ProfileEvent profileEvent = new ProfileEvent();
    protected GraphDataSource dataSource;
    protected int operationsPerTransaction;
    protected long counter = 0;
    protected int verboseLevel = 1;
    
    public AbstractOperation(int id,GraphDataSource dataSource,int operationsPerTransaction)
    {
        this.id = id;
        this.dataSource = dataSource;
        this.operationsPerTransaction = operationsPerTransaction;
    }

    public String getName()
    {
        return this.getClass().getName();
    }
    
    public ProfileEvent getProfileEvent()
    {
        return this.profileEvent;
    }

    public int getId()
    {
        return this.id;
    }

    public long getCounter()
    {
        return this.counter;
    }

    public List<LongPair> getResult()
    {
        return null;
    }
        
    public abstract void initialize(bench.common.AbstractBenchmark benchmark) throws Exception;
    public abstract void operate() throws Exception;
        
    public void run()
    {
        try
        {
            if(this.verboseLevel >= 2)
                System.out.printf("\t[%d] Started %s \n",this.id,this.getName());
            this.operate();
            if(this.verboseLevel >= 2)
                System.out.printf("\t[%d] Completed %s [%d]\n",this.id,this.getName(),counter);
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }
    }
}
