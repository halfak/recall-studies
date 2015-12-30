datasets/wikidata.human_revision_sample.tsv:
	wget http://tools.wmflabs.org/dexbot/res_aaron.txt -qO- | \
	tail -n+2 > \
	datasets/wikidata.human_revision_sample.tsv

datasets/wikidata.human_rev_reverted.tsv: datasets/wikidata.human_revision_sample.tsv
	cat datasets/wikidata.human_revision_sample.tsv | \
	editquality label_reverted \
		--host https://wikidata.org \
		--revert-radius 3 \
		--verbose > \
	datasets/wikidata.human_rev_reverted.tsv

datasets/wikidata.human_rev_reverted_proba.tsv: datasets/wikidata.human_rev_reverted.tsv
	(echo -e "rev_id\treverted"; \
	 cat datasets/wikidata.human_rev_reverted.tsv) | \
	python rs/score_revision.py https://ores.wmflabs.org wikidatawiki reverted > \
	datasets/wikidata.human_rev_reverted_proba.tsv
