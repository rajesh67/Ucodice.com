(function( factory ) {
	if ( typeof define === "function" && define.amd ) {

		// AMD. Register as an anonymous module.
		define([
			"jquery",
			"./core",
			"./mouse",
			"./widget"
		], factory );
	} else {

		// Browser globals
		factory( jQuery );
	}
}(function( $ ) {

return $.widget( "plans.timeslots", $.ui.mouse, {
	version: "@VERSION",
	widgetEventPrefix: "slide",

    options: {
        animate: false,
        distance: 0,
        max: 96,
        min: 0,
        orientation: "horizontal",
        range: false,
        step: 1,
        value: 0,
        values: null,
        intervals=null,

        // callbacks
        change: null,
        slide: null,
        start: null,
        stop: null
    },
    _create:function(){
        this.element
        //add a class for theming
            .addClass("timeslots-range");
        this.rightchanger=$('<img>',{
            "src":"/static/images/left.png",
        })
        .appendTo(this.element);

        this.leftchanger=$('<img>',{
            "src":"/static/images/right.png",
        })
        .appendTo(this.element);

        this._on(this.rightchanger,{
            click:"slideright"
        });

        this._on(this.leftchanger,{
            click:"slideleft"
        });
        this._refresh();
        var self=this,
            o=this.options,
            intervalslength=intervals.length;
        o.timeslots=this;

        function 
    },

    _createHandles:function(){
        var i,HandleCount_right,
            HandleCount_left,
            options=this.options,
            intervalslength=options.intervals.length,
            existingHandles_right = this.element.find( ".ui-slider-handle" ).addClass( "ui-slider-right" ),
            handle_right = "<span class='ui-slider-handle' tabindex='0' style='background:url(/static/images/left.png) no-repeat 100% 50% transparent;height:35px; margin-top:3px;'></span>",
            handle_left = "<span class='ui-slider-handle' tabindex='0' style='background:url(/static/images/right.png) no-repeat 100% 50% transparent;height:35px; margin-top:3px;'></span>",
            handles_right=[],
            handles_left=[],

        handleCount = ( options.values && options.values.length ) || 1;
        for (var v=0;v<intervalslength;v++){
            if((v%2)==1){
                HandleCount_right = ( options.intervals && options.intervals.length ) || 1;
            }else if((v%2)==0){
                HandleCount_left=( options.intervals && options.intervals.length ) || 1;
            }
        }
        
        /*for (var k=0;k<existingHandles.length;k++){
            if ((k%2)==0){    
                if ( existingHandles.length > HandleCount_right ) {
                    existingHandles.slice( HandleCount_right ).remove();
                    existingHandles = existingHandles.slice( 0, handleCount );
                }
            }
        }*/
        
        for (var j=0;j<existingHandles.length;i++){
            if((j%2)==1){
                handles_right.push(existingHandles[j]);
            }else if((j%2)==0){
                handles_left.push(existingHandles[j]);
            }
        }
        this.handlesright = existingHandles.add( $( handles_right.join( "" ) ).appendTo( this.element ) );
        this.handlesleft = existingHandles.add( $( handles_left.join( "" ) ).appendTo( this.element ) );

        var righhandleslength=this.handlesright.length;
        
        this.handleright = this.handlesright.eq( 0 );
        this.handleleft = this.handlesleft.eq( 0 );

        this.handlesright.each(function(key,value){
            $( this ).data( "ui-slider-handle-index", key );   
        });

        this.handlesleft.each(function(key,value){
            $( this ).data( "ui-slider-handle-index", i+righhandleslength );   
        });

        //should be deleted 




        for ( i = existingHandles.length; i < handleCount; i++ ) {

            handles.push( handle );
        }

        this.handles = existingHandles.add( $( handles.join( "" ) ).appendTo( this.element ) );

        this.handle = this.handles.eq( 0 );

        this.handles.each(function( i ) {
            $( this ).data( "ui-slider-handle-index", i );
    }
    ,


 	});
}));
