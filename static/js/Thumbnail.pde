public class Thumbnail{

   int index;
   public float plotX1,plotX2,plotY1,plotY2;
   boolean clicked;
   color c;


   float bg_lightness = 155;

   Thumbnail(int index, float x1, float y1, float x2, float y2){
     this.index = index;
     plotX1 = x1;
     plotX2 = x2;
     plotY1 = y1;
     plotY2 = y2;
     clicked = false;
    // c = map(
   }

   void drawThis(){
     strokeWeight(2);

     if(mouseOnThis() || clicked){
         if(bg_lightness <= 253) bg_lightness += 2;
         //fill(#FFFFFF);
         fill(bg_lightness);
         rect(plotX1,plotY1 - 1,plotX2,plotY2 + 1);
     }
     else{
         noStroke();
         if(bg_lightness >= 158) bg_lightness -= 3;
         //fill(#C0C0C0);
         fill(bg_lightness);
         rect(plotX1,plotY1 - 1,plotX2,plotY2 + 1); //a little interval
     }
   }

   boolean mouseOnThis(){
     return mouseX > plotX1 && mouseX < plotX2 && mouseY > plotY1 && mouseY < plotY2;
   }


   boolean _mouseClicked(){
     if(mouseOnThis()){
       currentColumn = index;
       println("clicked " + index);
       clicked = !clicked;
       return true;
     }
     return false;
   }
}
