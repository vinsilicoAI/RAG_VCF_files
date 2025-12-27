import os
import pysam
from langchain.docstore.document import Document

def load_vcfs(directory: str):
    """
    Iterates through all .vcf and .vcf.gz files in the given directory,
    parses them using pysam, and converts each variant record into a 
    text description wrapped in a LangChain Document.
    """
    documents = []
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        return []

    for filename in os.listdir(directory):
        if filename.endswith(".vcf") or filename.endswith(".vcf.gz"):
            filepath = os.path.join(directory, filename)
            try:
                # Open VCF file
                vcf = pysam.VariantFile(filepath)
                
                for record in vcf:
                    # Create a descriptive string for the variant
                    # Format: Chrom: <chrom>, Pos: <pos>, Ref: <ref>, Alts: <alts>, Qual: <qual>
                    chrom = record.chrom
                    pos = record.pos
                    ref = record.ref
                    alts = ", ".join(record.alts) if record.alts else "None"
                    qual = record.qual if record.qual else "N/A"
                    
                    # Extract INFO fields if needed, for now keeping it simple
                    info_str = "; ".join([f"{k}={v}" for k, v in record.info.items()])
                    
                    content = (
                        f"VCF File: {filename}\n"
                        f"Variant: Chromosome {chrom} at Position {pos}\n"
                        f"Reference Allele: {ref}\n"
                        f"Alternate Alleles: {alts}\n"
                        f"Quality: {qual}\n"
                        f"Info: {info_str}"
                    )
                    
                    metadata = {
                        "source": filename,
                        "chrom": chrom,
                        "pos": pos,
                        "qual": qual
                    }
                    
                    documents.append(Document(page_content=content, metadata=metadata))
                    
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                
    return documents
