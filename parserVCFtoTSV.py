#!/usr/bin/python
# coding: utf8

import sys
import os
from re import split,sub,match,search,I
from os.path import basename
from time import sleep,time #Execution time and slow downs
from scipy import stats #calcul p-value from z-score Test Wilcoxon
from subprocess import PIPE,Popen,call #exe command mode bash
#Global variable
Wilcoxon = "RankSum"
tsv=''
HG=''
Type='SNP' #By default
NGS='WGS'
Type='SNP' #By default
individu=''
#Mutation = Transition 1, Transversion 2, None=0
ID = {"B00HXC7":"DCP951","B00HZ6T":"DCP925","B00HXC9":"DCP521",
			"B00HXCA":"DCP750","B00HXD3":"DCP599","B00HXD4":"DCP713",
			"B00HXCD":"DCP714","B00HXCE":"CRO5875","B00HXCE":"CRO5878",
			"B00HXCF":"CRO5877","B00HXCG":"CRO5875","B00HXCH":"CRO5876",
			"B00HXCI":"CRO7702","B00HXCJ":"CRO7703","B00HXCK":"CRO7704",
			"B00HXCL":"CRO7705","B00HXCM":"CRO7706","B00HXCN":"CRO7707",
			"B00HXD5":"CRO7708","B00HXCP":"CRO6502","B00HXD6":"CRO6503",
			"B00HXD7":"CRO6504","B00HZ6R":"FMF3559","B00HZ6P":"FMF3557",
			"B00HZ6Q":"FMF3558","B00HXD8":"FMF3556","B00HXCW":"FMF3183",
			"B00HXCX":"FMF3358","B00HXCY":"FMF3359","B00HXCZ":"FMF3360",
			"B00HXD0":"FMF3361","B00HXD9":"FMF937","B00HXDA":"FMF3160"}
Colname= ['CHROM','START','ID','END','REF','ALT','QUAL','FILTRE','AC','AF','AN','DP','WGS','WES',
'Func.refGene_20170601','Gene.refGene_20170601','GeneDetail.refGene_20170601',
'ExonicFunc.refGene_20170601','AAChange.refGene_20170601',
'1000g2015all','1000g2015afr','1000g2015amr','1000g2015eur','1000g2015eas',
'1000g2015sas','dbSNP','downsampled','ExAC_ALL','ExAC_AFR', 'ExAC_AMR','ExAC_EAS','ExAC_FIN','ExAC_NFE','ExAC_OTH','ExAC_SAS','ExAC_nontcga_ALL',
'ExAC_nontcga_AFR','ExAC_nontcga_AMR', 'ExAC_nontcga_EAS','ExAC_nontcga_FIN','ExAC_nontcga_NFE',
'ExAC_nontcga_OTH', 'ExAC_nontcga_SAS','CNV','Ti-Tv','ExtExon','GC']

"""'phyloP46way_placental','phyloP100way_vertebrate',
'MLEAC','MLEAF','MQ','FS','BaseQRankSum','MQRankSum','ClippingRankSum','QD','SIFT_score',
'SIFT_pred','Polyphen2_HDIV_score','Polyphen2_HDIV_pred','Polyphen2_HVAR_score',
'Polyphen2_HVAR_pred','LRT_score','LRT_pred','MutationTaster_score',
'MutationTaster_pred','MutationAssessor_score','MutationAssessor_pred',
'FATHMM_score','FATHMM_pred','PROVEAN_score','PROVEAN_pred','VEST3_score',
'CADD_raw', 'CADD_phred','DANN_score','fathmm-MKL_coding_score','fathmm-MKL_coding_pred',
'MetaSVM_score','MetaSVM_pred','MetaLR_score','MetaLR_pred','integrated_fitCons_score',
'integrated_confidence_value','GERP++_RS','phyloP7way_vertebrate','phyloP20way_mammalian',
'phastCons7way_vertebrate','phastCons20way_mammalian','SiPhy_29way_logOdds','CLINSIG','CLNDBN','CLNACC','CLNDSDB',
'CLNDSDBID','RadialSVM_score','RadialSVM_pred','LR_score','LR_pred',
'gnomAD_exome_ALL','gnomAD_exome_AFR','gnomAD_exome_AMR','gnomAD_exome_ASJ',
'gnomAD_exome_EAS','gnomAD_exome_FIN','gnomAD_exome_NFE','gnomAD_exome_OTH',
'gnomAD_exome_SAS', 'dbscSNV_ADA_SCORE','dbscSNV_RF_SCORE','FILTER'
'ReadPosRankSum','SOR','ExcessHet',"""

def ouputCSV(fileCSV,individu):
	output = individu+'.csv'
	with open(output,"w") as o:
		o.write(fileCSV)
	os.system("chmod +x {}".format(output))
	return output
	
def mariaDB(File,table,Colname):
	purge="mysql -D pastelle -u pastelle --password=7SOlubl3ZH1sMlsN -e 'DROP TABLE IF EXISTS {};'".format(table)
	os.system(purge)
	colname_SQL=''
	for i in Colname:
		if i == Colname[-1]:
			colname_SQL=colname_SQL+"`{}` VARCHAR(512) NULL".format(i)
		elif match("AA",i):
			colname_SQL=colname_SQL+"`{}` TEXT(1000) NULL,".format(i)
		else:
			colname_SQL=colname_SQL+"`{}` VARCHAR(512) NULL,".format(i)
	command_CREATE = "mysql -D pastelle -u pastelle --password=7SOlubl3ZH1sMlsN -e 'CREATE TABLE IF NOT EXISTS {}({});'".format(table,colname_SQL)
	os.system(command_CREATE)
	
	command_COUNT="mysql -D pastelle -u pastelle --password=7SOlubl3ZH1sMlsN -e 'SELECT COUNT(*) FROM {};'".format(table)
	resultat_Count = os.popen(command_COUNT).read()
	resultat_Count = resultat_Count.rstrip("\n\r")
	count=split("\n",resultat_Count)
	if count.pop()!='0':
		Mariadb_UPDATE(File,table,colname)
	else:
		command_ALTER = "mysql -D pastelle -u pastelle --password=7SOlubl3ZH1sMlsN -e 'ALTER TABLE {} ADD COLUMN  IDs VARCHAR(512) UNIQUE FIRST;'".format(table)
		command_INSERT="mysql -D pastelle -u pastelle --password=7SOlubl3ZH1sMlsN -e 'UPDATE {} SET IDs=(SELECT SHA2(CONCAT(CHROM,\"_\",START,\"_\",END,\"_\",REF,\"_\",ALT),512));'".format(table)
		command_LOAD = "mysql -D pastelle -u pastelle --password=7SOlubl3ZH1sMlsN --local-infile=1 -e 'LOAD DATA LOCAL INFILE \"{}\" INTO TABLE {} FIELDS TERMINATED BY \"\t\" LINES TERMINATED BY \"\n\" IGNORE 1 ROWS;'".format(File,table)
		os.system(command_LOAD)
		print "Chargement fichier done"
		os.system(command_ALTER)
		print "Alteration de la table done"
		os.system(command_INSERT)
	mutation = ["mysql -D pastelle -u pastelle --password=7SOlubl3ZH1sMlsN -e 'update {} set `Ti-Tv`=1 where (REF=\"A\" OR REF=\"G\") AND (ALT=\"A\" OR ALT=\"G\");'",
	"mysql -D pastelle -u pastelle --password=7SOlubl3ZH1sMlsN -e 'update {} set `Ti-Tv`=1 where (REF=\"C\" OR REF=\"T\") AND (ALT=\"C\" OR  ALT=\"T\");'",
	"mysql -D pastelle -u pastelle --password=7SOlubl3ZH1sMlsN -e 'update {} set `Ti-Tv`=2 where REF=\"A\" AND (ALT=\"C\" OR  ALT=\"T\");'",
	"mysql -D pastelle -u pastelle --password=7SOlubl3ZH1sMlsN -e 'update {} set `Ti-Tv`=2 where REF=\"G\" AND (ALT=\"C\" OR ALT=\"T\");'",
	"mysql -D pastelle -u pastelle --password=7SOlubl3ZH1sMlsN -e 'update {} set `Ti-Tv`=2 where REF=\"C\" AND (ALT=\"A\" OR ALT=\"G\");'",
	"mysql -D pastelle -u pastelle --password=7SOlubl3ZH1sMlsN -e 'update {} set `Ti-Tv`=2 where REF=\"T\" AND (ALT=\"A\" OR ALT=\"G\");'"]
	for i in mutation:
		os.system(i.format(table))
	

def readFile(FilePath):
	""" Read file line by line and transfert to other function """
	print("Read file..........Work in progress")
	tsv=''
	tsv= "\t".join(Colname)
	tsv+= "\n"
	with open (FilePath,'r') as file: #Open the file in reading no writing allowed
		pos=''
		for line in file: #Read line by line
			if search("^chr",line): # Line with variant information
				"""" Create a tmp list lenght as colname full of NA. """
				line=line.rstrip("\n\r") #Clean recursion
				line=line.replace(";", "\t") #remove ";"
				line=line.replace(":","_") #remove : from annotation:annotated
				extract = split("\s",line) #Create list from line
				tsvLine=len(Colname)*["None"]
				j=0
				for i in range(8): #Complet de 7st first default columns 
					if i==3:
						tsvLine[i]="-";
						j-=1
					else: 
						tsvLine[i]=extract[j]
					j+=1
				
				for annotation in extract: # Loop in line to find Annotation
					#If Annotation have "=" add to data. Skip ANNOVAR date
					if search("=",annotation) and not search("ANNOVAR",annotation):
						
						info = split("=",annotation) #split ;annotation=value;
						
						if info[0] in Colname: # Check if annotation is in.
							if search(Wilcoxon,annotation):#if p-value < 0,05 reject H0. QUAL different, Biais sequencing
								info[1]=str(stats.norm.sf(abs(float(info[1])*2)))
								tsvLine[Colname.index(info[0])]=round(float(info[1]),6)
								
							elif match("AC",info[0]):#Change AC annotation
								if info[1]==2:
									tsvLine[Colname.index(info[0])]="Hom"
								else:
									tsvLine[Colname.index(info[0])]="Het"
							else:
								tsvLine[Colname.index(info[0])]=info[1] #add the 	value
			
						elif str(info[0])[0:-5] in Colname: # pour les annot _hg19/38
							tsvLine[Colname.index(str(info[0])[0:-5])]=info[1]
						if info[0] == "END":
							tsvLine[Colname.index("END")]=info[1]
							tsvLine[Colname.index("CNV")]="oui"
						if info[0] == "Type":						
							NGS = split("-",info[1])	
							if NGS[0] == "WGS":#Tag the WGS and WES statue
								tsvLine[Colname.index("WGS")]=1
							if NGS[1]=="WES":
								tsvLine[Colname.index("WES")]=1
								
					else:
						if annotation == "DS": #downsampled special annotation in ANNOVAR
							tsvLine[Colname.index("downsampled")]=1
						if annotation == "DB":#dbSNP special annotation in ANNOVAR
							tsvLine[Colname.index("dbSNP")]=1
				tsv = tsv +"\t".join(map(str,tsvLine))
				tsv+= "\n"
		tsv=tsv.replace("\t.","\tNone") #Tranform each . on Not Available
		
		#tsv=tsv.replace("\t", ";") #Line for biologist csv 
	return tsv

def extractor(table):
	selection = "mysql -D pastelle -u pastelle --password=7SOlubl3ZH1sMlsN -e 'SELECT * FROM {0} limit 300' > selection_{0}.txt".format(table)
	os.system(selection)
	#"mysql -D pastelle -u pastelle --password=7SOlubl3ZH1sMlsN -e 'SELECT `CHROM`,`START`,`END`,`ID`,`REF`,`ALT`,`FILTRE`,`AC`,`AF`,`AN`,`DP`,`Func.refGene_20170601`,`Gene.refGene_20170601`,`GeneDetail.refGene_20170601`,`ExonicFunc.refGene_20170601`,`AAChange.refGene_20170601`,`1000g2015all`,`1000g2015afr`,`1000g2015amr`,`1000g2015eur`,`1000g2015eas`,`1000g2015sas`,`ExcessHet`,`dbSNP`,`downsampled`,`ExAC_ALL`,`ExAC_AFR`,`ExAC_AMR`,`ExAC_EAS`,`ExAC_FIN`,`ExAC_NFE`,`ExAC_OTH`,`ExAC_SAS`,`ExAC_nontcga_ALL`,`ExAC_nontcga_AFR`,`ExAC_nontcga_AMR`,`ExAC_nontcga_EAS`,`ExAC_nontcga_FIN`,`ExAC_nontcga_NFE`,`ExAC_nontcga_OTH`,`ExAC_nontcga_SAS`,`WGS`,`WES`,`CNV` FROM CRO6502_HG19 limit 300' > selection_CRO6502_HG19.txt"
				
if __name__== '__main__':
	start = time()
	Input=sys.argv[1]
	File_name = split("\.",basename(Input))[0]
	tsv = readFile(Input)
	print("Output file is writing")
	ouputCSV(tsv,File_name)
	output = File_name+".csv"
	print("MySQL MariaDB")
	mariaDB(output,File_name,Colname)
	print("Creation fichier de selection")
	extractor(File_name)
	end = time()
	print('time : {:.2f}s'.format((end - start)))
