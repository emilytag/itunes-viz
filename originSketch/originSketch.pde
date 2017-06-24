// LIBRARIES
import processing.pdf.*;

// GLOBAL VARIABLES
PShape baseMap;
String csv[];
PFont f;
StringDict locs;
String allKeys[];

// SETUP
void setup() {
  size(2506,1396);
  //fullScreen(1);
  noLoop();
  f = createFont("Avenir-Medium", 12);
  baseMap = loadShape("/Users/EmilyTagtow/Documents/Python/Other/itunes-viz/World_map_with_nations.svg");
  csv = loadStrings("/Users/EmilyTagtow/Documents/Python/Other/itunes-viz/locations-collapsed-nums.tsv");
  locs = new StringDict();
  for(int i=0; i<csv.length; i++) {
    println(csv[i]);
    String location = csv[i].split("\t")[1];
    String longitude = csv[i].split("\t")[3];
    String latitude = csv[i].split("\t")[2];
    String count = csv[i].split("\t")[4];
    String locKey = location+"~"+longitude+"~"+latitude;
    if (!locs.hasKey(locKey)) {
    locs.set(locKey, count);
    
    }
  }
}

// DRAW
void draw() {
  beginRecord(PDF, "bands.pdf");
  shape(baseMap, 0, 0, width, height);
  noStroke();
  locs.sortValuesReverse();
  allKeys = locs.keyArray();
  for(int i=0; i<allKeys.length; i++){
    //textMode(MODEL);
    noStroke();
    String name = allKeys[i].split("~")[0];
    float longitude = float(allKeys[i].split("~")[1]);
    float latitude = float(allKeys[i].split("~")[2]);
    float count = float(locs.get(allKeys[i]));
    float graphLong = map(longitude, -180, 180, 0, width);
    float graphLat = map(latitude, 90, -90, 0, height);
    float markerSize = 9*sqrt(count)/PI;
    //float markerSize = 10.0;
    fill(255, 0, 0, 100);
    ellipse(graphLong, graphLat, markerSize, markerSize);
    
    if(count>34){
      fill(0);
      textFont(f);
      text(name, graphLong + markerSize + 5, graphLat + 4);
      noFill();
      stroke(0);
      line(graphLong+markerSize/2, graphLat, graphLong+markerSize, graphLat);
    }
  }
  endRecord();
  println("PDF Saved!");
}