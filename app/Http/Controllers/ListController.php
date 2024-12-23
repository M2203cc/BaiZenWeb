use League\Csv\Writer;
use SplTempFileObject;

public function export($id)
{
    $list = Lists::with('listDetails')->findOrFail($id);
    
    // 创建CSV writer
    $csv = Writer::createFromFileObject(new SplTempFileObject());
    
    // 添加CSV头部
    $csv->insertOne(['序号', '达人名称', 'URL']);
    
    // 添加数据行
    foreach ($list->listDetails as $index => $detail) {
        $csv->insertOne([
            $index + 1,
            $detail->name,
            $detail->url
        ]);
    }
    
    // 设置响应头
    $headers = [
        'Content-Type' => 'text/csv',
        'Content-Disposition' => 'attachment; filename="' . $list->name . '.csv"',
        'Pragma' => 'no-cache',
        'Cache-Control' => 'must-revalidate, post-check=0, pre-check=0',
        'Expires' => '0'
    ];
    
    return response($csv->toString(), 200, $headers);
} 