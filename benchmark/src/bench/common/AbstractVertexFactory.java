package bench.common;

import java.util.*;
import java.io.*;

public class AbstractVertexFactory
{
    private HashMap<Long,Long> objectMap = null;
    private String cacheName = "object_id.map";
    
    public AbstractVertexFactory(boolean useLocalMap)
    {
        if(useLocalMap)
            objectMap = new HashMap<Long,Long>();
    }

    public String getName()
    {
        return this.getClass().getName();
    }

    public boolean usesMap()
    {
        return (objectMap != null);
    }

    protected void put(long key,long id)
    {
        if(objectMap != null)
        {
            this.objectMap.put(key,id);
            System.out.printf("put %d,%d\n",key,id);
        }
    }

    public void setCacheName(String name)
    {
        this.cacheName = name;
    }

    public void initialize() throws IOException,ClassNotFoundException
    {
        if(objectMap != null)
            this.initialize(this.cacheName);
    }
    
    private synchronized void initialize(String fileName) throws IOException,ClassNotFoundException
    {
        if(fileName != null)
        {
            try
            {
                System.out.println("Start reading cache.");
                FileInputStream fileInputStream = new FileInputStream(fileName);
                ObjectInputStream objectInputStream = new ObjectInputStream(fileInputStream);
                objectMap = (HashMap<Long,Long>)objectInputStream.readObject();
                objectInputStream.close();
                System.out.println("End reading cache.");
            }
            catch(FileNotFoundException e)
            {
                System.out.printf("Cache file (%s) does not exist.\n",fileName);
            }
        }
    }
    
    private  synchronized void serialize(String fileName) throws FileNotFoundException,IOException
    {
        System.out.println("Start serialize");
        FileOutputStream fileOutputStream = new FileOutputStream(fileName);
        ObjectOutputStream stream = new ObjectOutputStream(fileOutputStream);
        stream.writeObject(objectMap);

         Iterator iterator =  objectMap.entrySet().iterator();
         while(iterator.hasNext())
         {
             Map.Entry pairs = (Map.Entry)iterator.next();
             long v = (Long)pairs.getKey();
             long id = (Long)pairs.getValue();
             System.out.printf("%d,%d\n",v,id);
         }
        
        stream.close();
        System.out.println("End serialize");
    }
    
    protected synchronized void remove(long key)
    {
        if(objectMap != null)
            this.objectMap.remove(key);
    }

    public void flush()throws FileNotFoundException,IOException
    {
        if(objectMap != null)
            this.serialize(this.cacheName);
    }

    public synchronized long getVertexId(long key)
    {
        long result = -1;
        try
        {
            result = this.objectMap.get(key);
        }
        catch(Exception e)
        {
        }
        return result;
    }
}
