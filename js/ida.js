 $(function(){
        csmapi.set_endpoint ('https://demo.iottalk.tw'); // 可以改url
        var profile = {
		    'dm_name': 'Dummy_Device',          
			'idf_list':[Dummy_Sensor],
			'odf_list':[Dummy_Control],
		        'd_name': 'd_name', // 需改名
        };
		
        function Dummy_Sensor(){
            return Math.random();
        }

        function Dummy_Control(data){
           $('.ODF_value')[0].innerText=data[0];
        }
      
/*******************************************************************/                
        function ida_init(){
	    console.log(profile.d_name);
	}
        var ida = {
            'ida_init': ida_init,
        }; 
        dai(profile,ida);     
});
