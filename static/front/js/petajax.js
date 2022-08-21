// 對jquery的ajax的封裝

'use strict';
var petajax = {
	'get':function(args) {
		args['method'] = 'get';
		this.ajax(args);
	},
	'post':function(args) {
		args['method'] = 'post';
		this.ajax(args);
	},
	'ajax':function(args) {
		// 設置csrftoken
		this._ajaxSetup();
		$.ajax(args);
	},
	'_ajaxSetup': function() {
		$.ajaxSetup({
			'beforeSend':function(xhr,settings) {
//			    如果不是以下請求
				if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
//				從meta標籤讀取csrfToken
						var csrftoken = $('meta[name=csrf-token]').attr('content');
//						設置到請求headers中
						xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
			}
		});
	}
};