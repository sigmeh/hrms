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
	$('#filename').html(filename);				//show file name
	$('#fileList').css({'display':'none'});				//close file list
	showingFileList = false;
	if (lastFile != filename){
		$('#fragmentsContainer').css({'display':'none'});						//reset display on file change
		$('#fragmentsContainerMessages').css({'display':'none'});				//		""
		$('#analyzePeakBox').css({'display':'block'});							//		""
		$('#messageBox').html('');												//
		$('#newFig').remove();													//remove old spectrum
		$('#spectrum').append('<img id="newFig"/>');							//reset spectrum
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
			showingData = true;			
			if (result.substring(0,4) == 'File'){					//error handling: Folder not found
				result = $('#filename').val() + ': ' + result;
				append(result);
			}	
			
			else{													//file was found and spectrum returned
				spectralData = JSON.parse(result);					//redefine spectralData in callback
				decompileData(spectralData);
				appendSpectralData(spectralData);	
				$('#newFig').attr('src',spectralData[0]);			//show new spectrum in DOM
				$('#sheet').css('display','block');					//display drawing sheet
			}			
		});

});
/*
$(document).on('mousedown','#sheet',function(e){
	var zoom = getCursorPos(e);
	mouseIsDown = true;
	drawZoom(e,true);
	$('#sheet').mousemove(function(e){
		if (mouseIsDown){
			var endzoom = getCursorPos(e);
			drawZoom(e,false);
		}
	});
});
function getCursorPos(e){
	if (e.pageX > 79 && e.pageX < 773 && e.pageY > 111 && e.pageY < 309){
		cursorX = e.pageX;
		cursorXadj = cursorX - 80;
		cursorY = e.pageY;
		cursorY = 309 - cursorY;
		cursorPos = cursorXadj + ', ' + cursorY;
		$('#cursor').html(cursorPos);
		return [cursorXadj,cursorY];
	}
}
*/

var mouseIsDown = false, zoomx1, zoomy1, drawing = false;
$(document).on('mousedown','#sheet',function(e){
	if (e.pageX >=76 && e.pageX <= 774 && e.pageY >= 110 && e.pageY <= 306){
		mouseIsDown = true;		
		zoomx1 = e.pageX;
		zoomy1 = e.pageY-70;
		var newZoom = document.createElement('div');
		newZoom.className = 'newZoom';
		newZoom.setAttribute('id','newZoom');
		newZoom.style.marginTop = zoomy1+'px';
		newZoom.style.marginLeft = zoomx1+'px';
		$('#sheet').append(newZoom);
	}
	
});
//draw zoom (mousemove on sheet)
$(document).on('mousemove','#sheet',function(e){
	if (mouseIsDown){
		drawing = true;	
		if (e.pageX >=76 && e.pageX <= 774 && e.pageY >= 110 && e.pageY <= 306){
			$('#newZoom').css({
				'width':Math.abs(e.pageX-zoomx1)+'px',
				'height':Math.abs(e.pageY-zoomy1)-70+'px'
			});
		}
		if (e.pageX < zoomx1){
			if (e.pageX < 76){
				$('#newZoom').css({'margin-left':76+'px'});
			}
			else{
				$('#newZoom').css({
					'margin-left':e.pageX+'px',
					'width':zoomx1-e.pageX+'px'
				});
			}
		}
		if (e.pageY -70 < zoomy1){
			if (e.pageY < 110){
				$('#newZoom').css({
					'margin-top':40+'px',
					'height':zoomy1-40+'px'
				});
			}
			else{
				$('#newZoom').css({
					'margin-top':e.pageY-70+'px',
					'height':zoomy1-(e.pageY-70)+'px'
				});
			}
		}
		if (e.pageX > 767){
			$('#newZoom').css({'width':767-zoomx1+'px'});
		}
		if (e.pageY > 306){
			$('#newZoom').css({'height':306-zoomy1-70+'px'});
		}
				
	}
});
function limitAdjust(num){
	return parseInt((1000*num))/1000.;
}
var figCount = 0;
//mouseup (on sheet) -- send new zoom to show.py
$(document).on('mouseup',function(){
	mouseIsDown = false;
	figCount++;		
	if (drawing){
		drawing = false;
		var xminNew = parseInt($('#newZoom').css('margin-left'))-76;
		var xmaxNew = parseInt($('#newZoom').css('width'))+xminNew;
		var yminNew = 198 - (parseInt($('#newZoom').css('margin-top'))-40)-parseInt($('#newZoom').css('height'));
		var ymaxNew = 198+40-(parseInt($('#newZoom').css('margin-top')));	
		if (yminNew<5){
			yminNew = 0
		}
		xminNew = limitAdjust(xminNew*(xmax-xmin)/690+xmin);
		xmaxNew = limitAdjust(xmaxNew*(xmax-xmin)/690+xmin);
		yminNew = limitAdjust(yminNew*(ymax-ymin)/198+ymin);
		ymaxNew = limitAdjust(ymaxNew*(ymax-ymin)/198+ymin);
		spectralData[0] = String($('#filename').val());
		spectralData[1] = xminNew;
		spectralData[2] = xmaxNew;
		spectralData[3] = yminNew;
		spectralData[4] = ymaxNew;
		$.ajax({
			method:'post',
			url:'cgi-bin/show.py',
			data:{'spectralData':JSON.stringify(spectralData)},
			success:function(result){
				$('#newZoom').remove();
				$('#messageBox').html('');
				spectralData = JSON.parse(result);			
				$('#newFig').attr('src',spectralData[0]+'?var='+figCount);		//prevent old fig cache
				appendSpectralData(spectralData);
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
$(document).on('click','#viewCandidates',function(){
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
}).on('click','#analyze',function(){				//analyze function for multi-peak auto-finder (original findRu results ported here)
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

function append(data){								//append new data to messageBox
	message = data + '<br>';
	$('#messageBox').append(message);
}

$(document).on('click','#addNewFrag',function(){
	//$('#addStop').prepend('<input type=\'checkbox\' class=\'checkbox\' id=\''+$('#newFragName').val()+'\'>'+$('#newFragName').val()+'<br>');
/*
	var newFragInput = document.createElement('input');
	newFragInput.type = 'checkbox';
	newFragInput.className = 'checkbox';
	newFragInput.id = $('#newFragName').val();
	console.log($('#newFragName').val());
	//$('#'+newFragInput.id).html(String(newFragName));
	$('#addNewFragBox').insertBefore(newFragInput+newFragInput.id+'<br>');
*/
});

$(document).on('click','#addNewFrag',function(){	//add user-generated fragment to list
	$.ajax({
		method:'post',
		url:'cgi-bin/add_frag.py',
		data:{'formula':JSON.stringify([$('#newFragName').val(),$('#newFragFormula').val()])},
		success:function(result){
			if (result == 'error'){
				$('#messageBox').append('Errors found in formula.');
			}
			else{
				$('#addStop').prepend('<input type=\'checkbox\' class=\'checkbox\' id=\''+$('#newFragName').val()+'\'>'+$('#newFragName').val()+'<br>');
			}
		}
	});
});

$(document).on('click','#analyzePeak',function(){
	$('#fragmentsContainer').css({'display':'none'});
	$('#fragmentsContainerMessages').css({'display':'none'});
	$('#analyzePeakBox').css({'display':'block'});
});

window.onload = function(){
	$.ajax({
		method:'post',
		url:'cgi-bin/get_frags.py',
		success:function(result){
			frags = JSON.parse(result);
			for (i=0;i<frags.length;i++){
				$('#addStop').prepend('<input type="checkbox" class="checkbox" id=\''+frags[i]+'\'>'+frags[i]+'<br>');
			}
		}
	});
}