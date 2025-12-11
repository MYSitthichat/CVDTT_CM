from fastapi import APIRouter, HTTPException
from database import get_db_connection
from schemas import AfterDeathData
from typing import Optional
import json

router = APIRouter(prefix="/after_death", tags=["After Death Services"])

@router.post("/save_after_death")
def save_after_death(data: AfterDeathData):
    """
    Save after death service data to database.
    EXACTLY matches old lab_manager system structure (server_api.py lines 225-507)
    """
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        
        # Use the actual sample_id sent from frontend (specimen_id)
        actual_sample_id = str(data.sample_id)
        
        # Build field mapping for lab_after_death table
        # Table structure: id, dtime, sample_id, status, updater, field1-field69
        fields = [''] * 69  # Initialize 69 empty fields
        
        # Parse service_data (comes as dict from new system)
        if isinstance(data.service_data, str):
            service_data = json.loads(data.service_data)
        else:
            service_data = data.service_data or {}
        
        
        # field1: Service type (CRITICAL - now supports multiple types)
        # Parse service_type which can be comma-separated: "Infectious Waste, Cremation, Jewelry"
        service_types = [s.strip() for s in data.service_type.split(',')]
        thai_types = []
        
        for stype in service_types:
            if stype == 'Infectious Waste':
                thai_types.append('ขยะติดเชื้อ')
            elif stype == 'Jewelry':
                thai_types.append('อัญมณี')
            elif stype == 'Cremation':
                thai_types.append('เผาซาก')
        
        # Join multiple service types with comma
        fields[0] = ', '.join(thai_types) if thai_types else 'None'
        
        # CRITICAL: Fields 2-15 are ALWAYS read for ALL service types (cremation section)
        cremation_details = service_data.get('cremation_details', {})
        
        # field2: cb_incineration (checkbox text)
        fields[1] = cremation_details.get('incineration', '')
        
        # field3: le_incineration_kg (weight from line edit)
        fields[2] = cremation_details.get('weight', '')
        
        # field4: cb_bone_storage (checkbox text)
        fields[3] = cremation_details.get('bone_storage', '')
        
        # field5: cb_ceremony (checkbox text)
        fields[4] = cremation_details.get('ceremony', '')
        
        # field6: dateEdit (date string DD/MM/YYYY)
        fields[5] = cremation_details.get('date', '')
        
        # field7: timeEdit (time string HH:mm)
        fields[6] = cremation_details.get('time', '')
        
        # field8: cb_diamond_mem (checkbox text)
        fields[7] = cremation_details.get('diamond', '')
        
        # field9: rb_fresh (radio button text)
        fields[8] = cremation_details.get('carcass_fresh', '')
        
        # field10: rb_autolysis (radio button text)
        fields[9] = cremation_details.get('carcass_autolysis', '')
        
        # field11: rb_unknown (radio button text)
        fields[10] = cremation_details.get('carcass_unknown', '')
        
        # field12: le_other_cond (line edit text)
        fields[11] = cremation_details.get('carcass_other', '')
        
        # field13: cb_necropsy (checkbox text)
        fields[12] = cremation_details.get('place_necropsy', '')
        
        # field14: le_place_opt1 (line edit text)
        fields[13] = cremation_details.get('place_other1', '')
        
        # field15: le_remark_lab (line edit text)
        fields[14] = cremation_details.get('remark', '')
        
        # field16: (reserved/unused)
        fields[15] = ''
        
        # INFECTIOUS WASTE FIELDS (field17-32)
        # Check if Infectious Waste is selected (can be part of multiple selections)
        waste_details = service_data.get('waste_details', {})
        if waste_details:  # If waste_details exists, process it
            items = waste_details.get('items', [])
            
            # Initialize
            tissues_text = ''
            tissues_qty = ''
            tissues_weight = ''
            needle_text = ''
            needle_qty = ''
            needle_weight = ''
            syringe_text = ''
            syringe_qty = ''
            syringe_weight = ''
            other1_name = ''
            other1_qty = ''
            other1_weight = ''
            other2_name = ''
            other2_qty = ''
            other2_weight = ''
            
            # Parse items - format: "checkbox_text: 5 qty 10 kg"
            for item in items:
                if 'Tissues' in item:
                    parts = item.split(':', 1)
                    tissues_text = parts[0].strip()
                    if len(parts) > 1:
                        details = parts[1].strip().split()  # Split by whitespace
                        # Parse "5 qty 10 kg" -> qty=5, weight=10
                        for i, word in enumerate(details):
                            if word == 'qty' and i > 0:
                                tissues_qty = details[i-1]
                            elif word == 'kg' and i > 0:
                                tissues_weight = details[i-1]
                            
                elif 'Needle' in item:
                    parts = item.split(':', 1)
                    needle_text = parts[0].strip()
                    if len(parts) > 1:
                        details = parts[1].strip().split()
                        for i, word in enumerate(details):
                            if word == 'qty' and i > 0:
                                needle_qty = details[i-1]
                            elif word == 'kg' and i > 0:
                                needle_weight = details[i-1]
                            
                elif 'Syringe' in item:
                    parts = item.split(':', 1)
                    syringe_text = parts[0].strip()
                    if len(parts) > 1:
                        details = parts[1].strip().split()
                        for i, word in enumerate(details):
                            if word == 'qty' and i > 0:
                                syringe_qty = details[i-1]
                            elif word == 'kg' and i > 0:
                                syringe_weight = details[i-1]
                else:
                    # Other items
                    if not other1_name:
                        parts = item.split(':', 1)
                        other1_name = parts[0].strip()
                        if len(parts) > 1:
                            details = parts[1].strip().split()
                            for i, word in enumerate(details):
                                if word == 'qty' and i > 0:
                                    other1_qty = details[i-1]
                                elif word == 'kg' and i > 0:
                                    other1_weight = details[i-1]
                    elif not other2_name:
                        parts = item.split(':', 1)
                        other2_name = parts[0].strip()
                        if len(parts) > 1:
                            details = parts[1].strip().split()
                            for i, word in enumerate(details):
                                if word == 'qty' and i > 0:
                                    other2_qty = details[i-1]
                                elif word == 'kg' and i > 0:
                                    other2_weight = details[i-1]
            
            # field17: cb_tissues
            fields[16] = tissues_text
            
            # field18: le_tissues_qty
            fields[17] = tissues_qty
            
            # field19: le_tissues_w
            fields[18] = tissues_weight
            
            # field20: cb_needle
            fields[19] = needle_text
            
            # field21: le_needle_qty
            fields[20] = needle_qty
            
            # field22: le_needle_w
            fields[21] = needle_weight
            
            # field23: cb_syringe
            fields[22] = syringe_text
            
            # field24: le_syringe_qty
            fields[23] = syringe_qty
            
            # field25: le_syringe_w
            fields[24] = syringe_weight
            
            # field26: le_inf_other1_name
            fields[25] = other1_name
            
            # field27: le_inf_other1_qty
            fields[26] = other1_qty
            
            # field28: le_inf_other1_w
            fields[27] = other1_weight
            
            # field29: le_inf_other2_name
            fields[28] = other2_name
            
            # field30: le_inf_other2_qty
            fields[29] = other2_qty
            
            # field31: le_inf_other2_w
            fields[30] = other2_weight
            
            # field32: le_inf_remark
            fields[31] = waste_details.get('remark', '')
        
        # JEWELRY FIELDS (field33-69)
        # Check if Jewelry is selected (can be part of multiple selections)
        jewelry_details = service_data.get('jewelry_details', {})
        if jewelry_details:  # If jewelry_details exists, process it
            
            # Get materials dictionary (new structure)
            materials = jewelry_details.get('materials', {})
            
            # Extract carcass data
            if 'carcass' in materials:
                fields[32] = materials['carcass'].get('text', '')      # field33: cb_gem_carcass
                fields[33] = materials['carcass'].get('qty', '')       # field34: le_gem_carcass_qty
                fields[34] = materials['carcass'].get('weight', '')    # field35: le_gem_carcass_w
            else:
                fields[32] = ''
                fields[33] = ''
                fields[34] = ''
            
            # Extract bone data
            if 'bone' in materials:
                fields[35] = materials['bone'].get('text', '')         # field36: cb_gem_bone
                fields[36] = materials['bone'].get('qty', '')          # field37: le_gem_bone_qty
                fields[37] = materials['bone'].get('weight', '')       # field38: le_gem_bone_w
            else:
                fields[35] = ''
                fields[36] = ''
                fields[37] = ''
            
            # Extract hair data
            if 'hair' in materials:
                fields[38] = materials['hair'].get('text', '')         # field39: cb_gem_hair
                fields[39] = materials['hair'].get('qty', '')          # field40: le_gem_hair_qty
                fields[40] = materials['hair'].get('weight', '')       # field41: le_gem_hair_w
            else:
                fields[38] = ''
                fields[39] = ''
                fields[40] = ''
            
            # Extract other1 data
            if 'other1' in materials:
                fields[41] = materials['other1'].get('text', '')       # field42: le_gem_other1_name
                fields[42] = materials['other1'].get('qty', '')        # field43: le_gem_other1_qty
                fields[43] = materials['other1'].get('weight', '')     # field44: le_gem_other1_w
            else:
                fields[41] = ''
                fields[42] = ''
                fields[43] = ''
            
            # Extract other2 data
            if 'other2' in materials:
                fields[44] = materials['other2'].get('text', '')       # field45: le_gem_other2_name
                fields[45] = materials['other2'].get('qty', '')        # field46: le_gem_other2_qty
                fields[46] = materials['other2'].get('weight', '')     # field47: le_gem_other2_w
            else:
                fields[44] = ''
                fields[45] = ''
                fields[46] = ''
            
            # Sizes (field48-53)
            size_str = jewelry_details.get('size', '')
            sizes = [s.strip() for s in size_str.split(',')] if size_str else []
            
            # field48: cb_size_lt1
            fields[47] = next((s for s in sizes if '<1 carat' in s), '')
            
            # field49: cb_size_1c
            fields[48] = next((s for s in sizes if '1 carat' in s and '<1' not in s), '')
            
            # field50: cb_size_2c
            fields[49] = next((s for s in sizes if '2 carat' in s), '')
            
            # field51: cb_size_3c
            fields[50] = next((s for s in sizes if '3 carat' in s), '')
            
            # field52: cb_size_4c
            fields[51] = next((s for s in sizes if '4 carat' in s), '')
            
            # field53: cb_size_5c
            fields[52] = next((s for s in sizes if '5 carat' in s), '')
            
            # Shapes (field54-60)
            shape_str = jewelry_details.get('shape', '')
            shapes = [s.strip() for s in shape_str.split(',')] if shape_str else []
            
            # field54: cb_shape_round
            fields[53] = next((s for s in shapes if 'round' in s.lower()), '')
            
            # field55: cb_shape_oval
            fields[54] = next((s for s in shapes if 'oval' in s.lower()), '')
            
            # field56: cb_shape_cushion
            fields[55] = next((s for s in shapes if 'cushion' in s.lower()), '')
            
            # field57: cb_shape_princess
            fields[56] = next((s for s in shapes if 'princess' in s.lower()), '')
            
            # field58: cb_shape_radiant
            fields[57] = next((s for s in shapes if 'radiant' in s.lower()), '')
            
            # field59: cb_shape_marquise
            fields[58] = next((s for s in shapes if 'marquise' in s.lower()), '')
            
            # field60: le_shape_other
            known_shapes = ['round', 'oval', 'cushion', 'princess', 'radiant', 'marquise']
            other_shapes = [s for s in shapes if not any(known in s.lower() for known in known_shapes)]
            fields[59] = ', '.join(other_shapes) if other_shapes else ''
            
            # Jewelry types (field61-66)
            jewelry_type_str = jewelry_details.get('jewelry_type', '')
            jewelry_types = [jt.strip() for jt in jewelry_type_str.split(',')] if jewelry_type_str else []
            
            # Ring
            ring_item = next((jt for jt in jewelry_types if 'ring' in jt.lower()), '')
            
            # field61: cb_acc_ring
            if ring_item:
                fields[60] = ring_item.split('(Code:')[0].strip()
            else:
                fields[60] = ''
            
            # field62: le_acc_code1
            if ring_item and 'Code:' in ring_item:
                fields[61] = ring_item.split('Code:')[1].strip().rstrip(')')
            else:
                fields[61] = ''
            
            # Necklace
            necklace_item = next((jt for jt in jewelry_types if 'necklace' in jt.lower()), '')
            
            # field63: cb_acc_necklace
            if necklace_item:
                fields[62] = necklace_item.split('(Code:')[0].strip()
            else:
                fields[62] = ''
            
            # field64: le_acc_code2
            if necklace_item and 'Code:' in necklace_item:
                fields[63] = necklace_item.split('Code:')[1].strip().rstrip(')')
            else:
                fields[63] = ''
            
            # Earring
            earring_item = next((jt for jt in jewelry_types if 'earing' in jt.lower() or 'earring' in jt.lower()), '')
            
            # field65: cb_acc_earing
            if earring_item:
                fields[64] = earring_item.split('(Code:')[0].strip()
            else:
                fields[64] = ''
            
            # field66: le_acc_code3
            if earring_item and 'Code:' in earring_item:
                fields[65] = earring_item.split('Code:')[1].strip().rstrip(')')
            else:
                fields[65] = ''
            
            # field67: le_color
            fields[66] = jewelry_details.get('color', '')
            
            # field68: le_price
            fields[67] = jewelry_details.get('price', '')
            
            # field69: pte_remark_gem
            fields[68] = jewelry_details.get('remark', '')
        
        # Build SQL INSERT statement with field1-field69
        field_names = ', '.join([f'field{i+1}' for i in range(69)])
        placeholders = ', '.join(['?'] * 69)
        sql = f"INSERT INTO lab_after_death (sample_id, updater, {field_names}) VALUES (?, ?, {placeholders})"
        
        # Execute with hardcoded sample_id='10' (matches old system)
        cursor.execute(sql, (actual_sample_id, data.updater, *fields))
        conn.commit()
        
        return {
            "message": "After death service data saved successfully",
            "sample_id": actual_sample_id,
            "service_type": data.service_type
        }
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving data: {str(e)}")
    finally:
        conn.close()

@router.get("/get_after_death/{sample_id}")
def get_after_death(sample_id: str):
    """Get after death service data by sample ID"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lab_after_death WHERE sample_id = ?", (sample_id,))
        result = cursor.fetchone()
        
        if not result:
            raise HTTPException(status_code=404, detail="Data not found")
        
        # Convert to dictionary (you'll need to map column names)
        return {"data": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving data: {str(e)}")
    finally:
        conn.close()