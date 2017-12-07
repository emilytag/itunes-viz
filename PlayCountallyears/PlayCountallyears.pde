
import processing.pdf.*;

FloatDict yearcount;
float max;
float min;
float xSpacer, ySpacer;
String[] years;

void setup() {
  size(1200,600);
  noLoop();
  String[] csv = loadStrings(args[0]);
  yearcount = new FloatDict();
  for(int i=1; i<csv.length; i++) {
    float playcount = float(csv[i].split("\t")[38]);
    String year = csv[i].split("\t")[79];
    if (!yearcount.hasKey(year) && playcount > 0 && year != "1958"){
      yearcount.set(year, playcount);
    }
    else{
      if (playcount > 0 && year != "1958") {
        float oldcount = yearcount.get(year);
        yearcount.set(year, playcount+oldcount);
      }
    }
  }
  max = max(yearcount.valueArray());
  min = 0;
  years = yearcount.keyArray();
}

void draw() {
  beginRecord(PDF, "allyears.pdf");
  fill(200);
  background(40);
  xSpacer = width / (years.length + 1);
  ySpacer = 100;
  
  //x-axis
  float xPos = (width - (xSpacer*(years.length)))/2;
  for(int x=1962; x<2018; x++){
    
    //draws line and text
    xPos = xPos + xSpacer;
    stroke(100);
    line(xPos, height-ySpacer, xPos, ySpacer);
    textSize(6);
    textAlign(CENTER);
    text(str(x), xPos, height - (ySpacer-10));
    
    //draws point for that year
    float graphHeight = (height-ySpacer) - ySpacer;
    float rawVal = yearcount.get(str(x));
    float adjVal = map(rawVal, min, max, 0, graphHeight);
    float yPoint = (height - ySpacer) - adjVal;
    noStroke();
    fill(255);
    ellipse(xPos, yPoint, 7, 7);
    
    //draws lines connecting points
    //change later to draw from current to previous to not duplicate calculations
    if (x < 2017){
      float nextVal = yearcount.get(str(x+1));
      float adjNext = map(nextVal, min, max, 0, graphHeight);
      float yNext = (height - ySpacer) - adjNext;
      stroke(255);
      line(xPos, yPoint, xPos + xSpacer, yNext);
    }
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
