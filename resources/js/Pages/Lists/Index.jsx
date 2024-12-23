// 在Action列中添加export按钮
<td className="px-6 py-4">
    <Link
        href={route("lists.show", list.id)}
        className="inline-flex items-center px-4 py-2 bg-gray-800 border border-transparent rounded-md font-semibold text-xs text-white uppercase tracking-widest hover:bg-gray-700"
    >
        View
    </Link>
    {/* 添加export按钮 */}
    <Link
        href={route("lists.export", list.id)}
        className="ml-2 inline-flex items-center px-4 py-2 bg-green-600 border border-transparent rounded-md font-semibold text-xs text-white uppercase tracking-widest hover:bg-green-500"
    >
        Export
    </Link>
</td>
  </rewritten_file> 