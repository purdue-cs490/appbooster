STable data;
float dataMin, dataMax;
float plotX1, plotY1;
float plotX2, plotY2;
float labelX,labelY;
float thumbx1,thumbx2;
int rowCount;
int columnCount;
int currentColumn = 0;
int yearMin, yearMax;
int[] years;
int yearInterval = 10;
int volumeInterval = 10;
int dif = 0;
PFont plotFont;

Integrator[] interpolators;

Thumbnail thumbnails[];
int volumeIntervalMinor = 5;


void setup() {

  size(1024, 768);
  data = new STable("../../static/js/stats.tsv");
  rowCount = data.getRowCount();
  columnCount = data.getColumnCount();

  years = int(data.getRowNames());
  yearMin = years[0];
  yearMax = years[years.length - 1];

  dataMin = 0;
  dataMax = data.getTableMax();

  // Corners of the plotted time series
  plotX1 = 80;
  plotX2 = width - 220;
  plotY1 = 60;
  plotY2 = height - plotY1;
  labelX = 50;
  labelY = height - 25;

  thumbx1 = plotX2 + 10;
  thumbx2 = width - 10;
  thumbnails = new Thumbnail[columnCount];
  initializeThumbnails();

  interpolators = new Integrator[rowCount];
  for (int row = 0; row < rowCount; row++) {
    float initialValue = data.getFloat(row, 0);
    interpolators[row] = new Integrator(initialValue);
    interpolators[row].attraction = 0.1;  // Set lower than the default
  }
  plotFont = createFont("SansSerif", 20);
  textFont(plotFont);

  smooth();
}


void draw() {
  background(224);

  // Show the plot area as a white box
  fill(255);
  rectMode(CORNERS);
  noStroke();
  rect(plotX1, plotY1, plotX2, plotY2);


  drawPanel();

  drawThumbnails();
}


void drawTitle() {
  fill(0);
  textSize(20);
  textAlign(LEFT);
  String title = data.getColumnName(currentColumn);
  text(title + "   peak value: " + data.getColumnMax(currentColumn) + " at:", plotX1, plotY1 - 10);

}


void drawYearLabels() {
  fill(0);
  textSize(10);
  textAlign(CENTER, TOP);

  // Use thin, gray lines to draw the grid
  stroke(224);
  strokeWeight(1);

  for (int row = 0; row < rowCount; row++) {
    if (years[row] % yearInterval == 0) {
      float x = map(years[row], yearMin, yearMax, plotX1, plotX2);
      text(years[row], x, plotY2 + 5);
      line(x, plotY1, x, plotY2);

    }
  }
}


void drawAxisLabels() {
  fill(0);
  textSize(8);
  textLeading(15);

  textAlign(CENTER, CENTER);
  text("Usage", labelX, (plotY1+plotY2)/2);
  textAlign(CENTER);
  text("Time", (plotX1+plotX2)/2, labelY);
}

void drawPanel(){

  drawTitle();
  drawYearLabels();
  drawAxisLabels();
  drawVolumeLabels();

  stroke(#5679C1);
  fill(#5679C1);
  for (int row = 0; row < rowCount; row++) {
    interpolators[row].update();
  }
  drawDataArea(currentColumn);
  noFill();

}

void setCurrent(int col) {
  currentColumn = col;

  for (int row = 0; row < rowCount; row++) {
    interpolators[row].target(data.getFloat(row, col));
  }
}

void drawDataPoints(int col, float plotX1, float plotY1, float plotX2, float plotY2) {
      for (int row = 0; row < rowCount; row++) {
          if (data.isValid(row, col)) {
          float value = data.getFloat(row, col);
          float x = map(years[row], yearMin, yearMax, plotX1, plotX2);
          float y = map(value, dataMin, dataMax, plotY2, plotY1);
          point(x, y);
      }
    }
}
void drawVolumeLabels() {
  fill(0);
  textSize(10);
  textAlign(RIGHT);

  stroke(128);
  strokeWeight(1);

  for (float v = dataMin; v <= dataMax; v += volumeIntervalMinor) {
    if (v % volumeIntervalMinor == 0) {     // If a tick mark
      float y = map(v, dataMin, dataMax, plotY2, plotY1);
      if (v % volumeInterval == 0) {        // If a major tick mark
        float textOffset = textAscent()/2;  // Center vertically
        if (v == dataMin) {
          textOffset = 0;                   // Align by the bottom
        } else if (v == dataMax) {
          textOffset = textAscent();        // Align by the top
        }
        text(floor(v), plotX1 - 10, y + textOffset);
        line(plotX1 - 4, y, plotX1, y);     // Draw major tick
      } else {
        //line(plotX1 - 2, y, plotX1, y);     // Draw minor tick
      }
    }
  }
}



void initializeThumbnails(){
    float yi1 = plotY1;
    float yi2 = yi1;
    for(int i = 0 ; i < columnCount; i++){
        yi2 =  map(i , -1 , columnCount - 1 , plotY1,  plotY2);
        thumbnails[i] = new Thumbnail(i, thumbx1, yi1, thumbx2, yi2);
        yi1 = yi2;
    }
}

void drawDataLine(int col) {
  beginShape();
  for (int row = 0; row < rowCount; row++) {
    if (data.isValid(row, col)) {
      float value = data.getFloat(row, col);
      float x = map(years[row], yearMin, yearMax, plotX1, plotX2);
      float y = map(value, dataMin, dataMax, plotY2, plotY1);
      vertex(x, y);
    }
  }
  endShape();
}

void drawThumbnails(){
     for(int i = 0; i < columnCount; i++){
         thumbnails[i].drawThis();
         strokeWeight(2);
         stroke(#5679C1);
         drawDataPoints(i, thumbnails[i].plotX1, thumbnails[i].plotY1,
         thumbnails[i].plotX2, thumbnails[i].plotY2);
     }

}

void drawDataArea(int col) {
  beginShape();
  for (int row = 0; row < rowCount; row++) {
    if (data.isValid(row, col)) {
      float value = interpolators[row].value;
      float x = map(years[row], yearMin, yearMax, plotX1, plotX2);
      float y = map(value, dataMin, dataMax, plotY2, plotY1);
      vertex(x, y);
    }
  }
  vertex(plotX2, plotY2);
  vertex(plotX1, plotY2);
  endShape(CLOSE);
}


boolean mouseInRect(float x1, float y1, float x2 , float y2){

    return (mouseX > x1) && (mouseX < x2) && (mouseY > y1) && (mouseY < y2);
}


void mouseClicked(){
  //println(mouseX + " " + mouseY);
   for(int i = 0 ; i < columnCount; i++)
      if(thumbnails[i]._mouseClicked())
        setCurrent(i);
}


void keyPressed() {
  if (key == '[') {
    currentColumn--;
    if (currentColumn < 0) {
      currentColumn = columnCount - 1;
    }
  } else if (key == ']') {
    currentColumn++;
    if (currentColumn == columnCount) {
      currentColumn = 0;
    }
  }
}
