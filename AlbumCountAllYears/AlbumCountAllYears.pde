
import processing.pdf.*;

FloatDict yearcount;
float max;
float min;
float xSpacer, ySpacer;
String[] years;
String[] csv;

void preProc(){
  ArrayList<String> albums = new ArrayList<String>();
  for(int i=1; i<csv.length; i++) {
    String album = csv[i].split("\t")[1];
    String year = csv[i].split("\t")[79];
    String uniq = album+"~"+year;
    if (!yearcount.hasKey(year) && year != "1958"){
      yearcount.set(year, 1);
    }
    else{
      if (year != "1958" && !albums.contains(uniq)) {
        float oldcount = yearcount.get(year);
        yearcount.set(year, oldcount+1);
      }
    }
   albums.add(uniq);
  }
}

void setup() {
  size(1200,600);
  csv = loadStrings("/Users/EmilyTagtow/Documents/Python/Other/itunes-viz/songs-1114.csv");
  yearcount = new FloatDict();
  preProc();
  max = max(yearcount.valueArray());
  min = 0;
  years = yearcount.keyArray();
}

void draw() {
  beginRecord(PDF, "AlbumCountAllYears.pdf");
  fill(200);
  background(40);
  xSpacer = width / (years.length + 1);
  ySpacer = 100;
  
  //x-axis
  float xPos = (width - (xSpacer*(years.length)))/2;
  for(int x=1962; x<2018; x++){
    
    //year text
    xPos = xPos + xSpacer;
    fill(100);
    textSize(6);
    textAlign(CENTER);
    text(str(x), xPos+(xSpacer/2), height - (ySpacer-10));
    
    //draws bar and label for that year
    float graphHeight = (height-ySpacer) - ySpacer;
    float rawVal = yearcount.get(str(x));
    float adjVal = map(rawVal, min, max, 0, graphHeight);
    float yPoint = (height - ySpacer) - adjVal;
    noStroke();
    fill(100);
    rect(xPos, yPoint, xSpacer-3, adjVal);
    text(str(int(rawVal)), xPos+(xSpacer/2), yPoint-3);
  }
  
  //min & max values
  textSize(8);
  textAlign(RIGHT);
  text(int(min), xSpacer+20, height - ySpacer);
  textAlign(RIGHT);
  text(int(max), xSpacer+20, ySpacer);
  
  
  //record pdf
  endRecord();
  println("PDF Saved!");
}