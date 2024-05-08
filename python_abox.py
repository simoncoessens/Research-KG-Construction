from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF
import pandas as pd

# Load the TBox definition
tbox_path = 'tbpx.ttl'
g = Graph()
g.parse(tbox_path, format='ttl')

# Paths to the actual CSV files
authors_csv_path = './data-from-lab1/authors.csv'
papers_csv_path = './data-from-lab1/papers_details_enriched.csv'
affiliations_csv_path = './data-from-lab1/affiliations.csv'
author_affiliations_csv_path = './data-from-lab1/affiliated_with.csv'

# Load CSV files into DataFrames
authors_df = pd.read_csv(authors_csv_path)
papers_df = pd.read_csv(papers_csv_path)
affiliations_df = pd.read_csv(affiliations_csv_path)
author_affiliations_df = pd.read_csv(author_affiliations_csv_path)

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
    graph.add((author_uri, EX.affiliatedwith, affiliation_uri))

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

# Export the graph to Turtle format
output_ttl_path = './output.ttl'
g.serialize(destination=output_ttl_path, format='turtle')

print(f'Graph exported to Turtle format at: {output_ttl_path}')
