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
            //System.out.printf("put %d,%d\n",key,id);
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
                //  System.out.print("Start reading cache.");
                FileReader fileReader = new FileReader(fileName);
                BufferedReader buffer = new BufferedReader(fileReader);
                String line = buffer.readLine();
                while(line != null)
                { 
                    String[] str = line.split(",");
                    Long a = Long.parseLong(str[0]);
                    Long b = Long.parseLong(str[1]);
                    //System.out.printf("%s,%s (%d,%d)\n",str[0],str[1],a,b);
                    objectMap.put(a,b);
                    line = buffer.readLine();
                }
                fileReader.close();
                //System.out.println(" End.");
            }
            catch(FileNotFoundException e)
            {
                System.out.printf("Cache file (%s) does not exist.\n",fileName);
            }
        }
    }
    
    private  synchronized void serialize(String fileName) throws FileNotFoundException,IOException
    {
        // System.out.print ("\t\tStart serialize");
        PrintWriter writer =  new PrintWriter(new FileWriter(fileName));
        Iterator iterator =  objectMap.entrySet().iterator();
         while(iterator.hasNext())
         {
             Map.Entry pairs = (Map.Entry)iterator.next();
             long v = (Long)pairs.getKey();
             long id = (Long)pairs.getValue();
             writer.printf("%d,%d\n",v,id);
         }
        
         //stream.close();
         writer.flush();
         writer.close();
         //System.out.println(" End");
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
