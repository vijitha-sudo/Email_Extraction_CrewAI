import os
import extract_msg

import os
import extract_msg
from fpdf import FPDF

from extraction import extract_data

def msg_to_pdf(msg_file_path, output_pdf_path,attachment_list,msg=None):
    """
    Converts a .msg file to a PDF document.

    Args:
        msg_file_path (str): The path to the .msg file.
        output_pdf_path (str): The path where the output PDF will be saved.
    """
    # Open the .msg file
    if not msg:
        msg = extract_msg.Message(msg_file_path)

    # Create a PDF object
    pdf = FPDF()
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=12)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Add email subject
    subject = msg.subject or "No Subject"
    pdf.cell(200, 10, txt=f"Subject: {subject}", ln=True, align='L')

    # Add sender information
    sender = msg.sender or "Unknown Sender"
    pdf.cell(200, 10, txt=f"From: {sender}", ln=True, align='L')

    # Add recipient information
    recipients = msg.to or "Unknown Recipient"
    pdf.cell(200, 10, txt=f"To: {recipients}", ln=True, align='L')

    # Add date
    date = msg.date or "Unknown Date"
    pdf.cell(200, 10, txt=f"Date: {date}", ln=True, align='L')

    # Add a line separator
    pdf.cell(200, 10, txt=" ", ln=True, align='L')
    # pdf.add_font("ArialUnicode", "", "Arial Unicode MS.TTF", uni=True)
    # pdf.set_font("ArialUnicode", size=12)

    

    # Add email body
    body = msg.body or "No Content"
    # text2 = body.encode('latin-1', 'replace').decode('latin-1')
    # Example: Decode to Unicode and encode back to UTF-8
    # body = body.encode('utf-8')
    # body = body.encode('latin-1', errors='replace').decode('latin-1')

# 
    pdf.multi_cell(0, 10, txt=body)

    # Save the PDF to file
    pdf.output(output_pdf_path)
    #print(f"PDF saved to: {output_pdf_path}")
    attachment_list.append(output_pdf_path)
    # Close the .msg file
    # msg.close()

def save_regular_attachment(attachment, download_folder,attachment_list):
    """
    Saves a regular (non-.msg) attachment to the specified folder.

    Args:
        attachment (extract_msg.attachment): The attachment to save.
        download_folder (str): The folder where the attachment will be saved.
    Returns:
        str: The path to the saved attachment file.
    """
    attachment_path = os.path.join(download_folder, attachment.name)
    
    with open(attachment_path, 'wb') as f:
        f.write(attachment.data)  # Write raw bytes
    #print(f"Downloaded: {attachment_path}")
    attachment_list.append(attachment_path)
    
    return attachment_path

def process_msg_attachment(attachment, download_folder,attachment_list):
    """
    Saves a .msg attachment and recursively processes its attachments.

    Args:
        attachment (extract_msg.attachment): The .msg attachment to save and process.
        download_folder (str): The folder where attachments will be saved.
    """
    msg_save_path = os.path.join(download_folder, attachment.name.split(".msg")[0])
    msg_attachment_path = os.path.join(download_folder, attachment.name)

    
    # Save the .msg attachment as a file
    # with open(msg_attachment_path, 'wb') as f:
    #     f.write(attachment.data)
    # attachment.save(customPath=msg_save_path)    
    
    #print(f"Saved nested .msg file: {msg_save_path}")
    pdf_filename = attachment.name.split(".msg")[0]+".pdf"
    pdf_path = os.path.join(download_folder, pdf_filename)
    #print(f"Converting {msg_attachment_path} to {pdf_path}")
    msg_to_pdf(msg_attachment_path, pdf_path,attachment_list,attachment.data)

    # Recursively process the saved .msg file
    # download_attachments_from_msg_file(msg_attachment_path, download_folder)

def recursive_method(attachments,download_folder,attachment_list):

    for attachment in attachments:
        if attachment.name.endswith(".msg"):
            # Handle nested .msg files
            process_msg_attachment(attachment, download_folder,attachment_list)
            recursive_method(attachment.data.attachments,download_folder,attachment_list)
            
        else:
            # Save regular attachments
            save_regular_attachment(attachment, download_folder,attachment_list)




def download_attachments_from_msg_file(msg_file_path,download_folder,attachment_list):
    """
    Recursively downloads attachments from a .msg file and processes nested .msg attachments.

    Args:
        msg_file_path (str): The path to the .msg file.
        download_folder (str): The folder where attachments will be saved.

    """

    # download_folder = os.path.join(download_folder, os.path.basename(msg_file_path).split(".msg")[0])
    # #print("download_folder:   ",download_folder)
    # Open the .msg file
    msg = extract_msg.Message(msg_file_path)
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # if file_name.endswith('.msg'):
    
    pdf_filename = msg_file_path.name.split(".msg")[0]+".pdf"
    pdf_path = os.path.join(download_folder, pdf_filename)
    #print(f"Converting {msg_file_path} to {pdf_path}")
    msg_to_pdf(msg_file_path, pdf_path,attachment_list,msg)
    

    # Iterate over the attachments in the .msg file
    recursive_method(msg.attachments,download_folder,attachment_list)

    # Close the .msg file
    msg.close()

def download_attachments_from_msg_folder(email_path, attachment_list,output_folder='temp'):
    """
    Downloads attachments from all .msg files in a specified folder, including handling nested .msg attachments.

    Args:
        folder_path (str): The path to the folder containing .msg files.
        download_folder (str): The folder where attachments will be saved.
    """
    # Ensure the download folder exists
    

    # Iterate over all files in the folder

    # for file_name in os.listdir(folder_path):        # Check if the file is a .msg file
        
    if os.path.basename(email_path.name).endswith(".msg"):
        # file_path = os.path.join(folder_path, file_name)
        #print(f"Processing file: {file_path}")
        # download_folder = os.path.join(output_folder)
        #print(download_folder)
        
        # Extract attachments from the .msg file
        download_attachments_from_msg_file(email_path,output_folder,attachment_list)

        # break
    
    return attachment_list


# Define the folder containing .msg files
# folder_path = r"C:\\Users\\czwkz5d\OneDrive - Allianz\\AGCS-FNOL Shared Folder\\email data"

# Define the folder to save attachments
# output_folder = r"temp"
# attachment_list = []
# # Call the function to download attachments
# attachment_list = download_attachments_from_msg_folder(email_path, output_folder)
#print("-----------------------------------------------------------------")
#print(attachment_list)


