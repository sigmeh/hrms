var spectralData, xmin, xmax, ymin, ymax, spectrumNP;

$(document).ready(function(){							//clear messages
	$('#clear').click(function(){
		$('#messageBox').html('');
	});
});
//this peak
$(document).on('click','#analyzePeak',function(){			//single peak (distribution) analysis
	$('#messageBox').html('');
});
//show_files
var showingFileList = false, lastFile = '';
$(document).on('click','#filesButton',function(){		//toggle file list on filesButton click
	$('#fileList').html('<b>./data_files/ </b><br>');
	if (showingFileList){								//if showing list, 
		$('#fileList').css({'display':'none'});			//	hide list
		showingFileList = false;
	}
	else{
		$.ajax({
			method:'post',
			url:'cgi-bin/show_files.py',				//show files.py
			success:function(result){
				file_list = JSON.parse(result);			//parse file_list from json object
				$('#fileList').css({'display':'block'});
				showingFileList = true;				
				for (i=0; i<file_list.length; i++){		//append each file to fileList as div with class 'file'
					$('#fileList').append('<div class="file">'+file_list[i]+'</div>');
				}
			}
		});
	}
});
//file click
$(document).on('click','.file',function(){				//select new file from list
	var filename = $(this).html();
	$('#filename').val(filename);				//show file name
	$('#fileList').css({'display':'none'});				//close file list
	showingFileList = false;
	if (lastFile != filename){
		$('#fragmentsContainer').css({'display':'none'});						//reset display on file change
		$('#fragmentsContainerMessages').css({'display':'none'});				//		""
		$('#analyzePeakBox').css({'display':'block'});							//		""
		$('#messageBox').html('');												//
		$('#newFig').remove();													//remove old spectrum
		$('#spectrum').append('<img id="newFig"/>');							//reset spectrum
		showingData = false;
	}
	
	lastFile = filename;
});
//format
$(document).on('click','#format',function(){			//format csv data (need to perform only once per data set)
	var info = $('#filename').val();
	$.ajax({
		method:'post',
		url: 'cgi-bin/format.py',						//fomats csv data; creates folder and adds new data files
		data: {'package':info}
	}).done(function(result){
		append(result);									//send result to messageBox
	});
});
//show
var showingData = false;
$(document).on('click','#show',function(){
		$('#messageBox').html('');
		var file = $('#filename').val();
		spectralData = [String(file), 0.0, 'full', 0, 100, 'NP'];	//send spectralData for full spectrum request
		$.ajax({													//ajax call to show spectrum
			method: 'post',
			url: 'cgi-bin/show.py',										
			data: {'spectralData':JSON.stringify(spectralData)}		//json-encode spectralData to send to show.py
		}).done(function(result){			
			if (result.substring(0,4) == 'File'){					//error handling: Folder not found
				result = $('#filename').val() + ': ' + result;
				append(result);
			}				
			else{													//file was found and spectrum returned
				showingData = true;	
				spectralData = JSON.parse(result);					//redefine spectralData in callback
				decompileData(spectralData);
				appendSpectralData(spectralData);	
				$('#newFig').attr('src',spectralData[0]);			//show new spectrum in DOM
				$('#sheet').css('display','block');					//display drawing sheet
			}			
		});

});
//zooming functionality (start zoom)
var mouseIsDown = false, zoomx1, zoomy1, drawing = false;
$(document).on('mousedown','#sheet',function(e){
	if (e.pageX >=76 && e.pageX <= 767 && e.pageY >= 110 && e.pageY <= 306){	//mouse is within zoom window
		mouseIsDown = true;		
		zoomx1 = e.pageX;											//origin x zoom
		zoomy1 = e.pageY-70;										//origin y zoom
		var newZoom = document.createElement('div');				//create zoom window
		newZoom.className = 'newZoom';
		newZoom.setAttribute('id','newZoom');
		newZoom.style.marginTop = zoomy1+'px';
		newZoom.style.marginLeft = zoomx1+'px';
		$('#sheet').append(newZoom);
	}
	
});
//draw zoom (mousemove on sheet)
$(document).on('mousemove','#sheet',function(e){					// while mouse is moving across zoom sheet 
	if (mouseIsDown){												// and the mouse is still down
		drawing = true;	
		if (e.pageX >=76 && e.pageX <= 767 && e.pageY >= 110 && e.pageY <= 306){	//within zoom window
			$('#newZoom').css({
				'width':Math.abs(e.pageX-zoomx1)+'px',								//get zoom width
				'height':Math.abs(e.pageY-zoomy1)-70+'px'							//get zoom height
			});
		}
		if (e.pageX < zoomx1){										//if zooming to the left of zoom (click) origin
			if (e.pageX < 76){										//if cursor is outside zoom window
				$('#newZoom').css({'margin-left':76+'px'});			//set zoom to minimum x value of zoom window
			}
			else{							
				$('#newZoom').css({									//zooming to the left; change margin-left to cursor position
					'margin-left':e.pageX+'px',
					'width':zoomx1-e.pageX+'px'
				});
			}
		}
		if (e.pageY -70 < zoomy1){									//cursor position is above zoom origin (y axis)
			if (e.pageY < 110){										//if cursor is above zoom window
				$('#newZoom').css({									//set zoom box to top of zoom window
					'margin-top':40+'px',
					'height':zoomy1-40+'px'
				});
			}
			else{													//otherwise set new margin-top to cursor position
				$('#newZoom').css({
					'margin-top':e.pageY-70+'px',
					'height':zoomy1-(e.pageY-70)+'px'
				});
			}
		}
		if (e.pageX > 767){											//if cursor is to the right of the zoom window
			$('#newZoom').css({'width':767-zoomx1+'px'});			//set to maximum x zoom
		}
		if (e.pageY > 306){											//if cursor is below zoom window
			$('#newZoom').css({'height':306-zoomy1-70+'px'});		//set to maximum y zoom (i.e., bottom of spectrum)
		}
				
	}
});
function limitAdjust(num){
	return parseInt((1000*num))/1000.;
}
var figCount = 0;
//mouseup (on sheet) -- send new zoom to show.py
$(document).on('mouseup',function(){										//on mouse up
	mouseIsDown = false;
	figCount++;		
	if (drawing){															//if drawing (zoom)
		drawing = false;
		var xminNew = parseInt($('#newZoom').css('margin-left'))-76;		//convert zoom DOM values to conventional plotting coordinates
		var xmaxNew = parseInt($('#newZoom').css('width'))+xminNew;
		var yminNew = 198 - (parseInt($('#newZoom').css('margin-top'))-40)-parseInt($('#newZoom').css('height'));
		var ymaxNew = 198+40-(parseInt($('#newZoom').css('margin-top')));	
		if (yminNew<5){
			yminNew = 0
		}
		xminNew = limitAdjust(xminNew*(xmax-xmin)/690+xmin);				//adjust to three decimal places and scale to appropriate data interval
		xmaxNew = limitAdjust(xmaxNew*(xmax-xmin)/690+xmin);				//	""
		yminNew = limitAdjust(yminNew*(ymax-ymin)/198+ymin);				//	""
		ymaxNew = limitAdjust(ymaxNew*(ymax-ymin)/198+ymin);				//	""
		spectralData[0] = String($('#filename').val());						// update spectralData with new information 
		spectralData[1] = xminNew;
		spectralData[2] = xmaxNew;
		spectralData[3] = yminNew;
		spectralData[4] = ymaxNew;
		$.ajax({
			method:'post',
			url:'cgi-bin/show.py',											//send new zoom parameters to show.py for processing
			data:{'spectralData':JSON.stringify(spectralData)},
			success:function(result){
				$('#newZoom').remove();											//remove zoom box
				$('#messageBox').html('');										//reset messages
				spectralData = JSON.parse(result);								//parse incoming data
				$('#newFig').attr('src',spectralData[0]+'?var='+figCount);		//prevent old fig cache
				appendSpectralData(spectralData);								//add new data to DOM
				decompileData(spectralData);
			}
		});
	}
});
/*
//y zoom
}).on('click','.arrow',function(){												//arrow functionality for y zoom, currently disabled
	if (showingData){
		if ($(this).attr('id') == 'arrow-up'){
			if (ymax > 20){
				ymax -= 20;
			}
			else{
				ymax -= 5;
			}
		}
		else{
			ymax += 20;
		}
		spectralData[0] = $('#filename').val();
		spectralData[4] = ymax;
		/*
		$.ajax({
			method:'post',
			url:'show.py',
			data:{'spectralData':JSON.stringify(spectralData)}
		}).done(function(result){
			$('#messageBox').html('');
			spectralData = JSON.parse(result);
			decompileData(spectralData);
			append(spectralData);
			$('#newFig').attr('src',spectralData[0]);
		});		
	}
	*/
//findRu
var RuPeaks;
$(document).on('click','#findRu',function(){								//invoke findRu.py to search data for ruthenium
	$('#messageBox').html('');												//	candidates based on isotopic distribution
	var filename = $('#filename').val();									//filename to check
	var threshold = $('#threshold').val();
	var missive = [filename, threshold];
	$('#fraglist').html('');
	$('#messageBox').append('Finding ruthenium... ');
	$.ajax({
		method:'post',
		url:'cgi-bin/findRu.py',											//call findRu.py
		data:{'package':JSON.stringify(missive)}							//send filename/threshold
	}).done(function(result){
		$('.fragButtons').css('display','inline-block');					//show analysis buttons on data return
		if (result.substring(0,4) == 'File' || result.substring(0,4) == 'Done'){	//error handling: file not formatted or not found
			append(filename + ': ' + result);
		}
		else{
			$('#messageBox').append('done <br>');
			$('#fragmentsContainer').css({'display':'block'});				//set data blocks
			$('#fragmentsContainerMessages').css({'display':'block'});		//		""
			$('#analyzePeakBox').css({'display':'none'});
			RuPeaks = JSON.parse(result);									//parse candidate list
			append("Total Number of Ruthenium Candidates Found: " + RuPeaks.length)		//add data to messageBox
			append("Major Ruthenium Peaks Ranked by Intensity: ");
			for (i = 0; i < RuPeaks.length; i++){							//display peak information
				append('Array Pos: ' + i + '; ' + RuPeaks[i][0][0].toFixed(4)+' m/z');
				$('#fraglist').append('<div><span>' + i + '</span> Peak: ' + RuPeaks[i][0][0].toFixed(4) + '</div>\n');
			}
			$('#fraglist div').first().attr('class','selected');			//select first element of list
			name = filename.substring(0, filename.length - 4);
		}
	});
});
//view Candidates (from findRu function)
$(document).on('click','#viewCandidates',function(){						//view Ru candidates from findRu in new window
 	var name = $('#filename').val();
 	name = name.substring(0,name.length-4);
	var newWindow = window.open("","_blank");
	newWindow.location.href = './data_files/' + name + '/' + name + '_RuCandidates.html';
});
$(document).on('click','#fraglist div',function(){
	$('.selected').removeClass('selected');
	$(this).addClass('selected');
}).on('click','#fragClear',function(){
	$('#fraglist').html('');
//fragment					(analyze)
}).on('click','#analyze',function(){							//analyze function for multi-peak auto-finder (original findRu results ported here)
	/*															//currently disabled
	var checkboxes = document.getElementsByClassName('checkbox');		
	var checkFragments = [];									//get list of fragments to check
	for (i = 0; i < checkboxes.length; i++){
		if (checkboxes[i].checked){
			checkFragments.push(checkboxes[i].getAttribute('id'));
		}
	}
	var peakToCheck = $('#fraglist').find('.selected').find('span').html();
	var fragPack = [];
	fragPack.push(RuPeaks[Number(peakToCheck)]);
	fragPack.push(checkFragments);
	$.ajax({
		method:'post',
		url:'cgi-bin/fragment.py',
		data:{'fragPack':JSON.stringify(fragPack)}
	}).done(function(result){
		appendFrag(result);
		var output = $('#fragmentsMessages').val();
		var candidate = output.indexOf('Candidate:');
		var end = output.indexOf('endAppend');	
		append('output length: ' + output.length);			
		append(output.substring(candidate,end));
	});
	*/
}).on('click','#fragMessageClear',function(){
	$('#fragmentsMessages').val('');
});

function appendSpectralData(spectralData){			//parse spectral data to append to messageBox
	append('File: ' + spectralData[0]);
	append('xmin: ' + spectralData[1]);
	append('xmax: ' + spectralData[2]);
	append('ymin: ' + spectralData[3]);
	append('ymax: ' + spectralData[4]);
	append('Number of Points: ' + spectralData[5]);
}

var figurename;
function decompileData(spectralData){				//set global variables from spectralData
	figurename = spectralData[0];
	xmin = spectralData[1];
	xmax = spectralData[2];
	ymin = spectralData[3];
	ymax = spectralData[4];
	spectrumNP = spectralData[5];
}

function appendFrag(data){
	$('#fragmentsMessages').val(data);
}

function append(data){													//append new data to messageBox
	message = data + '<br>';
	$('#messageBox').append(message);
}

$(document).on('click','#addNewFrag',function(){						//add user-generated fragment to list
	$.ajax({
		method:'post',
		url:'cgi-bin/add_frag.py',										//call add_frag.py
		data:{'formula':JSON.stringify([$('#newFragName').val(),$('#newFragFormula').val()])},	//send name and formula
		success:function(result){
			if (result == 'error'){
				$('#messageBox').append('Errors found in formula.');	//error handling
			}
			else{														//add new fragment checkbox to DOM
				$('#addStop').append('<input type=\'checkbox\' class=\'checkbox\' id=\''+$('#newFragName').val()+'\'>'+$('#newFragName').val()+'<br>');
			}
		}
	});
});

$(document).on('click','#analyzePeak',function(){
	if (showingData){
		$('#fragmentsContainer').css({'display':'none'});
		$('#fragmentsContainerMessages').css({'display':'none'});
		$('#analyzePeakBox').css({'display':'block'});
		var filename = $('#filename').val();
		spectralData[0] = filename;
		frag_selections = $('.analyzePeakCheck');
		var check_frags = [];									//list of fragments to analyze
		for (i=0;i<frag_selections.length;i++){
			if(frag_selections[i].checked){
				check_frags.push(frag_selections[i].id);
			}
		}
		
		$.ajax({
			method:'post',
			url:'./cgi-bin/analyze_peak.py',
			data:{'package':JSON.stringify([spectralData,check_frags])},
			success:function(result){
				if (result == 'error'){
					append('There was an error in the request.');
				}
				else{
					console.log(result);
				}
			}
		});
	}
});

window.onload = function(){
	$.ajax({
		method:'post',
		url:'cgi-bin/get_frags.py',										// get fragments from ref/fragments.txt and add to DOM (on window load)
		success:function(result){
			frags = JSON.parse(result);
			for (i=0;i<frags.length;i++){
				$('#addStop').prepend('<input type="checkbox" class="checkbox analyzePeakCheck" id=\''+frags[i]+'\'>'+frags[i]+'<br>');	//add each fragment
			}
		}
	});
}