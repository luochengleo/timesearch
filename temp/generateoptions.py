fout = open('option.txt','w')
for i in range(1,51,1):
    fout.write('<option value="'+str(i)+'">'+str(i)+'</option>\n')
fout.close()