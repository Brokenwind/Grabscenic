#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct{
  char name[10];
  unsigned int date;
}Birth;

unsigned int reverse(char *line){
  int len = strlen(line);
  int re[3];
  int sp = 0;
  int i,j;
  for (i = 0,j = 0; i < len; i++){
    if (line[i] == '/'){
      line[i] = '\0';
      re[j++] = atoi(line+sp);
      sp = i + 1;
    }
  }
  re[j] = atoi(line+sp);
  return re[0]*10000 + re[1]*100 + re[2];
}

int main(){
  int num;
  int i;
  char line[30];
  char name[10];
  Birth* list;
  Birth max,min;
  int count = 0;
  unsigned int ret;
  unsigned int ldate = 1814*10000 + 9 * 100 + 6;
  unsigned int cdate = 2014*10000 + 9 * 100 + 6;

  scanf("%d",&num);
  list = (Birth*)malloc(sizeof(Birth)*num);
  for (i = 0; i < num; i++){
    scanf("%s",name);
    scanf("%s",line);
    ret = reverse(line);
    if (ret >= ldate && ret <= cdate){
      strcpy(list[count].name,name);
      list[count++].date = ret;
    }
  }
  max = list[0];
  min = list[0];
  for (i = 0; i< count; i ++){
    if (max.date > list[i].date)
      max = list[i];
    if (min.date < list[i].date)
      min = list[i];
  }
  /**if not process it
     格式错误
   */
  if (count == 0)
    printf("0\n");
  else
    printf("%d %s %s\n",count,max.name,min.name);
  return 0;
}

