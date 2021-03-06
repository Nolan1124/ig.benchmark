package bench.common;
import java.util.*;
import java.io.*;

public class GraphDataSource
{
    private int scale;
    private String edgeListPath = null;
    private String searchListPath = null;

    private BufferedReader edgeListReader = null;
    private BufferedReader searchListReader = null;
    
    private int block = 0;
    private long offset = 0;
    private boolean useSize = false;
    
    public GraphDataSource(int scale,
                           String edgeListPath,
                           String searchListPath,
                           boolean useSize
                           )
    {
        this.scale = scale;
        this.edgeListPath =  edgeListPath;
        this.searchListPath = searchListPath;
        this.useSize = useSize;
    }
    
    public boolean initialize() throws FileNotFoundException
    {
        if(edgeListPath != null)
            this.edgeListReader = new BufferedReader(new FileReader(edgeListPath));
        if(searchListPath != null)
            this.searchListReader = new BufferedReader(new FileReader(searchListPath));
        this.offset = this.block * this.getSize();
        return true;
    }

    public void setBlock(int value)
    {
        this.block = value;
    }
    
    public int getBlock()
    {
        return this.block;
    }

    public long getOffset()
    {
        return this.offset;
    }
    
    public long getScale()
    {
        return scale;
    }
    
    public long getSize()
    {
        if(useSize)
            return scale;
        return 1 << scale;
    }

    public boolean hasEdgeList()
    {
        return (edgeListReader != null);
    }
    
    public LongPair getNextPair(BufferedReader reader)
    {
        LongPair edgePair = null;
        try
        {
            String line = reader.readLine();
            //System.out.printf("LINE: %s\n",line);
            if(line != null)
            {
                String[] fields = line.split(",");
                long first  = Long.parseLong(fields[0].trim());
                long second  = Long.parseLong(fields[1].trim());
                edgePair = new LongPair(first,second);
            }
        }
        catch (java.io.EOFException e)
        {
            return null;
        }
        catch (java.io.IOException ioe)
        {
            return null;
        }
        return edgePair;
    }


    public Long getNextVertexID(BufferedReader reader)
    {
        Long vertexID = null;
        try
        {
            String line = reader.readLine();
            if(line != null)
            {
                long id  = Long.parseLong(line);
                vertexID = new Long(id);
            }
        }
        catch (java.io.EOFException e)
        {
            return null;
        }
        catch (java.io.IOException ioe)
        {
            return null;
        }
        return vertexID;
    }
    
    public synchronized List<LongPair> getNextEdgePair(int size)
    {
        List<LongPair> edgePairContainer = new ArrayList<LongPair>();
        if(edgeListReader != null)
        {
            int counter = 0;
            boolean done = false;
            while(!done)
            {
                LongPair edgePair = this.getNextPair(edgeListReader);
                if((edgePair != null) && (edgePair.getFirst() != edgePair.getSecond()))
                {
                    edgePairContainer.add(edgePair);
                    counter += 1;
                }
                done = (counter >= size) || (edgePair == null);
            }
        }
        return edgePairContainer;
    }
    
    
    public synchronized List<Long> getNextSearchList(int size)
    {
        List<Long> searchContainer = new ArrayList<Long>();
        if(searchListReader != null)
        {
            int counter = 0;
            boolean done = false;
            while(!done)
            {
                Long vertexID = this.getNextVertexID(searchListReader);
                if(vertexID != null)
                {
                    searchContainer.add(vertexID);
                    counter += 1;
                }
                done = (counter >= size) || (vertexID == null);
            }
        }
        return searchContainer;
    }
    
}
