package bench.common;

public interface AbstractOperationFactory{
    public AbstractOperation create(int i,GraphDataSource graphDataSource,int tsize);
}
