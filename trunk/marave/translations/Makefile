TRANSLATIONS=marave_es.ts marave_he.ts marave_de.ts marave_pl.ts
TRANSLATED=marave_es.qm marave_he.qm marave_de.qm marave_pl.qm

all: update_trans $(TRANSLATED)

marave_es.qm: marave_es.ts
	lrelease marave_es.ts -compress -qm marave_es.qm
marave_he.qm: marave_he.ts
	lrelease marave_he.ts -compress -qm marave_he.qm
marave_de.qm: marave_de.ts
	lrelease marave_de.ts -compress -qm marave_de.qm
marave_pl.qm: marave_pl.ts
	lrelease marave_pl.ts -compress -qm marave_pl.qm
	
update_trans:
	pylupdate4 ../*py -ts $(TRANSLATIONS)
	@for ts in ${TRANSLATIONS};\
	do \
	  sed 's/filename="/filename="..\//g' -i $$ts;\
	done
