package bench.common;
import java.util.*;
import java.io.*;


import java.lang.Math;
import java.util.*;
import java.lang.management.*;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;

public class ProfileEvent{
    private long startTime = 0;
    private long stopTime = 0;
    private boolean running = false;
    private double rate = -1;
    private long size = 0;

    public void start()
    {
        this.startTime = System.currentTimeMillis();
        this.running = true;
    }
    
    public void save(String fileName,String name,int threads,long txSize,String indexType,long databaseSize) throws Exception
    {
        String osType= System.getProperty("os.name").replace(' ','_').toLowerCase();
        //String fileName = String.format("%s.profile",name);
        PrintWriter writer =  new PrintWriter(new FileWriter(fileName,true));
        writer.println(this.format(osType,name,threads,txSize,indexType,databaseSize));
        writer.flush();
        writer.close();
    }
    
    public String format(String osType,String operation,int threads,long txSize,String indexType,long databaseSize)
    {
        return String.format("{\"os\":\"%s\",\"operation\":\"%s\",\"time\":%d,\"threads\":%d,\"opsize\":%d,\"rate\":%.2f,\"txsize\":%d,\"index\":\"%s\",\"size\":%d,\"mem_init\":%2.0f,\"mem_used\":%2.0f,\"mem_committed\":%2.0f,\"mem_max\":%2.0f}",
                             osType,
                             operation,
                             this.getElapsedTime(),
                             threads,
                             this.getSize(),
                             this.getRate(),
                             txSize,
                             indexType,
                             databaseSize,
                             ProfileEvent.GetMemoryUsageInit(),
                             ProfileEvent.GetMemoryUsageUsed(),
                             ProfileEvent.GetMemoryUsageCommitted(),
                             ProfileEvent.GetMemoryUsageMax()
                             );
    }



    private static MemoryMXBean memorymxBean;
    static
    {
        ProfileEvent.memorymxBean = ManagementFactory.getMemoryMXBean();
    }
    public static double GetMemoryUsageInit(){
        return (ProfileEvent.memorymxBean.getHeapMemoryUsage().getInit());
    }
    
    public static double GetMemoryUsageUsed(){
        return (ProfileEvent.memorymxBean.getHeapMemoryUsage().getUsed());
    }
    
    public static double GetMemoryUsageCommitted(){
        return (ProfileEvent.memorymxBean.getHeapMemoryUsage().getCommitted());
    }
    
    public static double GetMemoryUsageMax(){
        return (ProfileEvent.memorymxBean.getHeapMemoryUsage().getMax());
    }

    
    public void stop()
    {
        this.stopTime = System.currentTimeMillis();
        this.running = false;
    }

    public void stop(long size)
    {
        this.stop();
        this.size = size;
        long e = this.getElapsedTime();
        if((size > 0) && (e > 0))
        {
            double _size = (double)this.size;
            double _t = (double)e; 
            this.rate = 1000.0*_size/_t;
        }
    }

    public long getElapsedTime()
    {
        long elapsed;
        if (running)
        {
            elapsed = (System.currentTimeMillis() - startTime);
        }
        else
        {
            elapsed = (stopTime - startTime);
        }
        return elapsed;
    }

    public long getSize()
    {
        return this.size;
    }
    
    public double getRate()
    {
        return this.rate;
    }

    public double getRate(int size)
    {
        long e = this.getElapsedTime();
        if((size > 0) && (e > 0))
        {
            return 1000.0*size/e;
        }
        return -1;
    }
    
    public long getElapsedTimeSecs()
    {
        long elapsed;
        if (running)
        {
            elapsed = ((System.currentTimeMillis() - startTime) / 1000);
        }
        else
        {
            elapsed = ((stopTime - startTime) / 1000);
        }
        return elapsed;
    }

}
