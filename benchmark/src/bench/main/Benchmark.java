package bench.main;

import java.util.*;
import java.io.*;
import org.apache.commons.cli.*;
import bench.common.*;

public class Benchmark
{
    protected Options options = new Options();
    protected CommandLine commandLine = null;
    protected String operation = null;
    protected AbstractBenchmark benchmark = null;
       
    public Benchmark()
    {
    }
    
    @SuppressWarnings("static-access")
    private void initialize()
    {
        final String helpMessage   = "print this message.";
        final String engineMessage = "DB engine (ig2|ig3)";
        final String scaleMessage  = "vertex size 2^scale.";
        final String sizeMessage  = "vertex size.";
        final String vitMessage    = String.format("number of vertex ingest threads [default=%d].",AbstractBenchmark.DefaultNumberOfThreads);
        final String eitMessage    = String.format("number of edge ingest threads [default=%d].",AbstractBenchmark.DefaultNumberOfThreads);
        final String tMessage    = String.format("number of operation threads [default=%d].",AbstractBenchmark.DefaultNumberOfThreads);
        final String txSizeMessage = String.format("transaction size (number of elements per transaction). [default=%d].",AbstractBenchmark.DefaultTransactionSize);
        final String newMessage    = "create new database before ingest";
        final String blockMessage  = "block number (default = 0)";
        final String operationMessage = "Operation [create|delete|standard_ingest|standard_e_ingest|accelerated_ingest|accelerated_e_ingest|search|bfs|dfs]";
        final String indexMessage = "IndexType [none|gr|ge|lu]";
        final String useLocalMapMessage = "Use local map to cache object id";
        final String edgelistMessage = "file path for edge-list file";
        final String searchlistMessage = "search path for edge-list file, used for search|traversal|delete";
        final String limitMessage = "Navigation Path limit";
        final String dbMessage = String.format("Database name [default=%s].",AbstractBenchmark.DefaultDatabaseName);
        final String propertyMessage = String.format("file path of the property name [default=%s].",AbstractBenchmark.DefaultPropertyFile);
        final String serverMessage = String.format("server uri used for the rest-neo engine [default=%s].",AbstractBenchmark.DefaultServerURI);
        final String verboseMessage = String.format("Verbose level (default:1)");
        final String profileMessage = String.format("Profile file name");
        
        options.addOption(new Option("help",helpMessage));
        options.addOption(OptionBuilder.withArgName("integer").hasArg().withDescription(verboseMessage).create("verbose"));
        options.addOption(OptionBuilder.withArgName("string").hasArg().withDescription(engineMessage).create("engine"));
        options.addOption(OptionBuilder.withArgName("integer").hasArg().withDescription(scaleMessage).create("scale"));
        options.addOption(OptionBuilder.withArgName("integer").hasArg().withDescription(sizeMessage).create("size"));
        options.addOption(OptionBuilder.withArgName("integer").hasArg().withDescription(vitMessage).create("vit"));
        options.addOption(OptionBuilder.withArgName("integer").hasArg().withDescription(eitMessage).create("eit"));
        options.addOption(OptionBuilder.withArgName("integer").hasArg().withDescription(tMessage).create("t"));
        options.addOption(OptionBuilder.withArgName("integer").hasArg().withDescription(txSizeMessage).create("tsize"));
        options.addOption(OptionBuilder.withArgName("integer").hasArg().withDescription(newMessage).create("new"));
        options.addOption(OptionBuilder.withArgName("integer").hasArg().withDescription(blockMessage).create("block"));
        options.addOption(OptionBuilder.withArgName("string").hasArg().withDescription(operationMessage).create("operation"));
        options.addOption(OptionBuilder.withArgName("string").hasArg().withDescription(indexMessage).create("index"));
        options.addOption(OptionBuilder.withArgName("file-path").hasArg().withDescription(edgelistMessage).create("edgelist"));
        options.addOption(OptionBuilder.withArgName("file-path").hasArg().withDescription(searchlistMessage).create("searchlist"));
        options.addOption(OptionBuilder.withArgName("string").hasArg().withDescription(dbMessage).create("db"));
        options.addOption(OptionBuilder.withArgName("string").hasArg().withDescription(propertyMessage).create("property"));
        options.addOption(OptionBuilder.withArgName("integer").hasArg().withDescription(limitMessage).create("limit"));
        options.addOption(OptionBuilder.withArgName("string").hasArg().withDescription(serverMessage).create("server"));
        options.addOption(OptionBuilder.withArgName("string").hasArg().withDescription(profileMessage).create("profile"));
        options.addOption(new Option("uselocalmap",useLocalMapMessage));
        options.addOption(new Option("ascii","Use ascii format for edge and search list."));
    }
    
    private void showHelp(String programName)
    {
        HelpFormatter formatter = new HelpFormatter();
        formatter.setWidth(100);
        formatter.printHelp(programName,options);
    }

    
    private boolean process(String programName,String[] arguments)
    {
        CommandLineParser parser = new PosixParser();
        try
        {
            commandLine = parser.parse( options, arguments);
        }
        catch (ParseException e)
        {
            e.printStackTrace();
            this.showHelp(programName);
            return false;
        }
        if(this.commandLine.hasOption("help"))
        {
            this.showHelp(programName);
            return false;
        }
        else
        {
            String value = this.commandLine.getOptionValue("engine");
            if(value == null)
            {
                System.out.println("'engine' is required use either 'ig2|ig3'");
                return false;
            }
            else if(value.equalsIgnoreCase("ig2"))
                this.benchmark = new bench.ig2.IGBenchmark();
            else if(value.equalsIgnoreCase("ig3"))
                this.benchmark = new bench.ig3.IGBenchmark();
            else{
                System.out.println("'engine' is required use either 'ig2|ig3'");
                return false;
            }
            this.operation = this.commandLine.getOptionValue("operation");
            if(this.operation == null)
            {
                this.showHelp(programName);
                return false;
            }
           
        }
        return true;
    }

    private void setupBenchmark() throws Exception
    {
        int verboseLevel = (Integer.parseInt(this.commandLine.getOptionValue("verbose",new Integer(1).toString())));
        int scale = (Integer.parseInt(this.commandLine.getOptionValue("scale",new Integer(-1).toString())));
        int size =  (Integer.parseInt(this.commandLine.getOptionValue("size",new Integer(-1).toString())));
        int tsize = (Integer.parseInt(this.commandLine.getOptionValue("tsize",new Integer(10000).toString())));
        int numberOfVertexIngestThreads = (Integer.parseInt(this.commandLine.getOptionValue("vit",new Integer(AbstractBenchmark.DefaultNumberOfThreads).toString())));
        int numberOfEdgeIngestThreads = (Integer.parseInt(this.commandLine.getOptionValue("eit",new Integer(AbstractBenchmark.DefaultNumberOfThreads).toString())));
        int numberOfThreads = (Integer.parseInt(this.commandLine.getOptionValue("t",new Integer(AbstractBenchmark.DefaultNumberOfThreads).toString())));
        String edgeListPath = this.commandLine.getOptionValue("edgelist");
        String searchListPath = this.commandLine.getOptionValue("searchlist");
        int limit = (Integer.parseInt(this.commandLine.getOptionValue("limit",new Integer(AbstractBenchmark.DefaultLimit).toString())));
        boolean ascii = this.commandLine.hasOption("ascii");
        boolean useSize = false;
        
        if(scale == -1)
        {
            scale = size;
            useSize = true;
        }
        
        GraphDataSource dataSource = new GraphDataSource(scale,edgeListPath,searchListPath,useSize);
        String dbName = this.commandLine.getOptionValue("db",AbstractBenchmark.DefaultDatabaseName);
        String propertyFileName = this.commandLine.getOptionValue("property",AbstractBenchmark.DefaultPropertyFile);
        String server = this.commandLine.getOptionValue("server",AbstractBenchmark.DefaultServerURI);
        int block = (Integer.parseInt(this.commandLine.getOptionValue("block",new Integer(0).toString())));


        dataSource.setBlock(block);
        this.benchmark.setProfileFileName(this.commandLine.getOptionValue("profile"));
        this.benchmark.setVerboseLevel(verboseLevel);
        this.benchmark.setTransactionSize(tsize);
        this.benchmark.setGraphDataSource(dataSource);
        this.benchmark.setNumberOfVertexIngestThreads(numberOfVertexIngestThreads);
        this.benchmark.setNumberOfEdgeIngestThreads(numberOfEdgeIngestThreads);
        this.benchmark.setNumberOfThreads(numberOfThreads);
        this.benchmark.setUseLocalCache(this.commandLine.hasOption("uselocalmap"));
        this.benchmark.setIndexType(AbstractBenchmark.parseIndexType(this.commandLine.getOptionValue("index")));
        this.benchmark.setLimit(limit);
        this.benchmark.setDbName(dbName);
        this.benchmark.setPropertyFileName(propertyFileName);
        this.benchmark.setServerURI(server);
        dataSource.initialize();
        this.benchmark.initialize();
        if(verboseLevel > 1)
            System.out.println(this.benchmark.toString());
    }

    
    public void run() throws Exception
    {
        this.setupBenchmark();
        if(this.operation.equalsIgnoreCase("create"))
        {
            this.benchmark.createDB();
            this.benchmark.closeDB();
        }
        else if(this.operation.equalsIgnoreCase("delete"))
        {
            this.benchmark.initialize();
            this.benchmark.deleteDB();
        }
        else if(this.operation.equalsIgnoreCase("accelerated_ingest"))
        {
            int createNew = (Integer.parseInt(this.commandLine.getOptionValue("new",new Integer(0).toString())));
            if(createNew > 0)
            {
                this.benchmark.createDB();
            }
            else{
                this.benchmark.openDB();
            }
            
            this.benchmark.acceleratedIngest();
            this.benchmark.flush();
            this.benchmark.closeDB();
        }
        else if(this.operation.equalsIgnoreCase("accelerated_e_ingest"))
        {
            this.benchmark.openDB();
            this.benchmark.acceleratedEdgeIngest();
            this.benchmark.closeDB();
        }
        else if(this.operation.equalsIgnoreCase("standard_ingest"))
        {
            int createNew = (Integer.parseInt(this.commandLine.getOptionValue("new",new Integer(0).toString())));
            if(createNew > 0)
            {
                this.benchmark.createDB();
            }
            else
            {
                this.benchmark.openDB();
            }
            this.benchmark.standardIngest();
            this.benchmark.flush();
            this.benchmark.closeDB();
        }
        else if(this.operation.equalsIgnoreCase("standard_e_ingest"))
        {
            this.benchmark.openDB();
            this.benchmark.standardEdgeIngest();
            this.benchmark.flush();
            this.benchmark.closeDB();
        }
        else if(this.operation.equalsIgnoreCase("search"))
        {
            this.benchmark.openDB();
            this.benchmark.search(false);
            this.benchmark.closeDB();
        }
        else if(this.operation.equalsIgnoreCase("read"))
        {
            this.benchmark.openDB();
            this.benchmark.read();
            this.benchmark.closeDB();
        }
        else if(this.operation.equalsIgnoreCase("bfs"))
        {
            this.benchmark.openDB();
            this.benchmark.bfsTraverse();
            this.benchmark.closeDB();
        }
        else if(this.operation.equalsIgnoreCase("dfs"))
        {
            this.benchmark.openDB();
            this.benchmark.dfsTraverse();
            this.benchmark.closeDB();
        }
        else if(this.operation.equalsIgnoreCase("remove"))
        {
            this.benchmark.openDB();
            this.benchmark.remove();
            this.benchmark.closeDB();
        }
        else if(this.operation.equalsIgnoreCase("status"))
        {
            this.benchmark.databaseStatus();
        }
        else{
            System.out.println("Error: Unknown operation type");
            this.showHelp(Benchmark.class.getName());
        }
    }
    
    public static void main(String[] args) throws Exception
    {
        Benchmark runner = new Benchmark(); 
        runner.initialize();
        
        if(runner.process(Benchmark.class.getName(),args))
        {
            runner.run();
        }
    }
}








