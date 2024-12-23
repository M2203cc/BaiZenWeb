// 添加导出路由
Route::get('/lists/{list}/export', [ListController::class, 'export'])->name('lists.export');