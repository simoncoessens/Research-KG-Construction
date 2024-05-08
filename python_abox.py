from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF
import pandas as pd
import random

# Load the TBox definition
tbox_path = 'tbpx.ttl'
g = Graph()
g.parse(tbox_path, format='ttl')

# Paths to the actual CSV files
authors_csv_path = 'data-from-lab1/authors.csv'
papers_csv_path = 'data-from-lab1/papers_details_enriched.csv'
affiliations_csv_path = 'data-from-lab1/affiliations.csv'
author_affiliations_csv_path = 'data-from-lab1/affiliated_with.csv'
cited_by_csv_path = 'data-from-lab1/citations.csv'
written_by_csv_path = 'data-from-lab1/written_by_enriched.csv'
conferences_csv_path = 'data-from-lab1/conferences_enriched.csv'
journals_csv_path = 'data-from-lab1/journals_enriched.csv'
published_in_csv_path = 'data-from-lab1/published_in.csv'
reviews_csv_path = 'data-from-lab1/reviews.csv'
reviewed_by_csv_path = 'data-from-lab1/reviewed_by.csv'
review_on_csv_path = 'data-from-lab1/review_on.csv'

# Load CSV files into DataFrames
authors_df = pd.read_csv(authors_csv_path)
papers_df = pd.read_csv(papers_csv_path)
affiliations_df = pd.read_csv(affiliations_csv_path)
author_affiliations_df = pd.read_csv(author_affiliations_csv_path)
cited_by_df = pd.read_csv(cited_by_csv_path)
written_by_df = pd.read_csv(written_by_csv_path)
conferences_df = pd.read_csv(conferences_csv_path)
journals_df = pd.read_csv(journals_csv_path)
published_in_df = pd.read_csv(published_in_csv_path)
reviews_df = pd.read_csv(reviews_csv_path)
reviewed_by_df = pd.read_csv(reviewed_by_csv_path)
review_on_df = pd.read_csv(review_on_csv_path)

# Define the namespace for our data
EX = Namespace('http://www.gra.fo/schema/untitled-ekgauthor')
g.bind('ex', EX)

# Function to add affiliation data to the graph
def add_affiliation_to_graph(graph, name, affiliation_type, address, email, phone_number, website):
    affiliation_uri = EX[f'affiliation/{name.replace(" ", "_").lower()}']
    graph.add((affiliation_uri, RDF.type, EX.Affiliation))
    graph.add((affiliation_uri, EX.name, Literal(name)))
    graph.add((affiliation_uri, EX.type, Literal(affiliation_type)))
    graph.add((affiliation_uri, EX.address, Literal(address)))
    graph.add((affiliation_uri, EX.email, Literal(email)))
    graph.add((affiliation_uri, EX.phone_number, Literal(phone_number)))
    graph.add((affiliation_uri, EX.website, Literal(website)))
    return affiliation_uri

# Function to add author data to the graph
def add_author_to_graph(graph, author_id, name, email):
    author_uri = EX[f'author/{author_id}']
    graph.add((author_uri, RDF.type, EX.Author))
    graph.add((author_uri, EX.authorId, Literal(author_id)))
    graph.add((author_uri, EX.name, Literal(name)))
    graph.add((author_uri, EX.email, Literal(email)))
    return author_uri

# Function to link authors with affiliations
def link_author_to_affiliation(graph, author_id, affiliation_name):
    author_uri = EX[f'author/{author_id}']
    affiliation_uri = EX[f'affiliation/{affiliation_name.replace(" ", "_").lower()}']
    graph.add((author_uri, EX.affiliatedWith, affiliation_uri))

# Function to add paper data to the graph
def add_paper_to_graph(graph, paper_id, title, abstract, year, doi, author_name, author_email):
    paper_uri = EX[f'paper/{paper_id}']
    graph.add((paper_uri, RDF.type, EX.Paper))
    graph.add((paper_uri, EX.paperId, Literal(paper_id)))
    graph.add((paper_uri, EX.title, Literal(title)))
    graph.add((paper_uri, EX.abstract, Literal(abstract)))
    graph.add((paper_uri, EX.year, Literal(year, datatype='http://www.w3.org/2001/XMLSchema#integer')))
    graph.add((paper_uri, EX.doi, Literal(doi)))
    author_uri = EX[f'author/{author_email.lower()}']
    graph.add((paper_uri, EX.writtenBy, author_uri))
    return paper_uri

# Function to add citation data to the graph
def add_citation_to_graph(graph, paper_id, reference_id, year):
    paper_uri = EX[f'paper/{paper_id}']
    reference_uri = EX[f'paper/{reference_id}']
    graph.add((paper_uri, EX.citedBy, reference_uri))
    graph.add((paper_uri, EX.citationYear, Literal(year, datatype='http://www.w3.org/2001/XMLSchema#integer')))

# Function to link paper authors
def link_paper_author(graph, paper_id, author_id):
    paper_uri = EX[f'paper/{paper_id}']
    author_uri = EX[f'author/{author_id}']
    graph.add((paper_uri, EX.writtenBy, author_uri))

# Define research areas
research_areas = ["Databases", "Machine Learning", "Network Security", "Artificial Intelligence"]

# Function to randomly assign a research area
def assign_research_area():
    return random.choice(research_areas)


# Function to add conference data to the graph
def add_conference_to_graph(graph, name, url):
    name = name.replace(" ", "")
    conference_uri = EX[f'conference/{name}']
    graph.add((conference_uri, RDF.type, EX.Conference))
    graph.add((conference_uri, EX.url, Literal(url) if url else Literal("")))
    graph.add((conference_uri, EX.area, Literal(assign_research_area())))
    return conference_uri

# Function to add conference edition data to the graph
def add_conference_edition_to_graph(graph, ss_venue_id, edition, year, name):
    name = name.replace(" ", "")
    conference_uri = EX[f'conference/{name}']
    edition_uri = EX[f'conference_edition/{ss_venue_id}']
    graph.add((edition_uri, RDF.type, EX.ConferenceEdition))
    graph.add((edition_uri, EX.editionNumber, Literal(edition, datatype='http://www.w3.org/2001/XMLSchema#integer')))
    graph.add((edition_uri, EX.partOfConference, conference_uri))
    graph.add((edition_uri, EX.editionYear, Literal(year, datatype='http://www.w3.org/2001/XMLSchema#integer')))
    return edition_uri

# Function to add journal data to the graph
def add_journal_to_graph(graph, name, url):
    name = name.replace(" ", "")
    journal_uri = EX[f'journal/{name}']
    graph.add((journal_uri, RDF.type, EX.Journal))
    graph.add((journal_uri, EX.url, Literal(url) if url else Literal("")))
    graph.add((journal_uri, EX.area, Literal(assign_research_area())))
    return journal_uri

# Function to add journal volume data to the graph
def add_journal_volume_to_graph(graph, ss_venue_id, volume, year, name):
    name = name.replace(" ", "")
    journal_uri = EX[f'journal/{name}']
    volume_uri = EX[f'journal_volume/{ss_venue_id}']
    graph.add((volume_uri, RDF.type, EX.JournalVolume))
    graph.add((volume_uri, EX.volumeNumber, Literal(volume, datatype='http://www.w3.org/2001/XMLSchema#integer')))
    graph.add((volume_uri, EX.partOfJournal, journal_uri))
    graph.add((volume_uri, EX.ss_venue_id, Literal(ss_venue_id)))
    graph.add((volume_uri, EX.year, Literal(year, datatype='http://www.w3.org/2001/XMLSchema#integer')))
    return volume_uri

# Function to add review data to the graph
def add_review_to_graph(graph, review_id, decision, date, abstract):
    review_uri = EX[f'review/{review_id}']
    graph.add((review_uri, RDF.type, EX.Review))
    graph.add((review_uri, EX.reviewId, Literal(review_id)))
    graph.add((review_uri, EX.decision, Literal(decision)))
    graph.add((review_uri, EX.date, Literal(date, datatype='http://www.w3.org/2001/XMLSchema#date')))
    graph.add((review_uri, EX.abstract, Literal(abstract)))
    return review_uri

# Function to link a paper to a review
def link_review_to_paper(graph, review_id, paper_id):
    review_uri = EX[f'review/{review_id}']
    paper_uri = EX[f'paper/{paper_id}']
    graph.add((review_uri, EX.reviewsPaper, paper_uri))

# Function to link a review to an author (reviewer)
def link_review_to_author(graph, review_id, author_id):
    review_uri = EX[f'review/{review_id}']
    author_uri = EX[f'author/{author_id}']
    graph.add((review_uri, EX.reviewedBy, author_uri))

# Function to link a paper to a conference edition or journal volume
def link_paper_to_venue(graph, paper_id, ss_venue_id):
    paper_uri = EX[f'paper/{paper_id}']
    venue_uri = EX[f'conference_edition/{ss_venue_id}'] if (EX[f'conference_edition/{ss_venue_id}'], RDF.type, EX.ConferenceEdition) in graph else EX[f'journal_volume/{ss_venue_id}']
    graph.add((paper_uri, EX.publishedIn, venue_uri))

# Add affiliations to the graph
for _, row in affiliations_df.iterrows():
    add_affiliation_to_graph(
        g,
        row['name'],
        row['type'],
        row['address'],
        row['email'],
        row['phone_number'],
        row['website']
    )

# Add authors to the graph
for _, row in authors_df.iterrows():
    add_author_to_graph(
        g,
        row['authorId'],
        row['name'],
        row['email']
    )

# Link authors to affiliations
for _, row in author_affiliations_df.iterrows():
    link_author_to_affiliation(g, row['authorId'], row['affiliation'])

# Add papers to the graph
for _, row in papers_df.iterrows():
    add_paper_to_graph(
        g,
        row['paperId'],
        row['title'],
        row['abstract'],
        row['year'],
        row['doi'],
        row['MA_name'],
        row['MA_email']
    )

# Add citations to the graph
for _, row in cited_by_df.iterrows():
    add_citation_to_graph(
        g,
        row['paperId'],
        row['referenceId'],
        row['year']
    )

# Link papers with their authors
for _, row in written_by_df.iterrows():
    link_paper_author(
        g,
        row['paperId'],
        row['authorId']
    )

# Add conferences and their editions to the graph
for _, row in conferences_df.iterrows():
    conference_uri = add_conference_to_graph(
        g,
        row['name'],
        row['url']
    )
    add_conference_edition_to_graph(
        g,
        row['ss_venue_id'],
        row['edition'],
        row['year'],
        row['name']
    )

# Add journals and their volumes to the graph
for _, row in journals_df.iterrows():
    journal_uri = add_journal_to_graph(
        g,
        row['name'],
        row['url']
    )
    add_journal_volume_to_graph(
        g,
        row['ss_venue_id'],
        row['volume'],
        row['year'],
        row['name']
    )

# Link papers to conference editions or journal volumes
for _, row in published_in_df.iterrows():
    link_paper_to_venue(g, row['paper_id'], row['ss_venue_id'])

# Add reviews to the graph
for _, row in reviews_df.iterrows():
    add_review_to_graph(
        g,
        row['review_id'],
        row['decision'],
        row['date'],
        row['abstract']
    )

# Link reviews to authors (reviewers)
for _, row in reviewed_by_df.iterrows():
    link_review_to_author(
        g,
        row['review_id'],
        row['author_id']
    )

# Link reviews to papers
for _, row in review_on_df.iterrows():
    link_review_to_paper(
        g,
        row['review_id'],
        row['paper_id']
    )

# Export the graph to Turtle format
output_ttl_path = './output.ttl'
g.serialize(destination=output_ttl_path, format='turtle')

print(f'Graph exported to Turtle format at: {output_ttl_path}')