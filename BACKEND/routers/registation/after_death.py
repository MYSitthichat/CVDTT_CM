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
        
        # CRITICAL: Old system uses hardcoded sample_id='10' for compatibility
        # Override whatever sample_id was sent
        actual_sample_id = '10'
        
        # Build field mapping for lab_after_death table
        # Table structure: id, dtime, sample_id, status, updater, field1-field69
        fields = [''] * 69  # Initialize 69 empty fields
        
        # Parse service_data (comes as dict from new system)
        if isinstance(data.service_data, str):
            service_data = json.loads(data.service_data)
        else:
            service_data = data.service_data or {}
        
        # FIELD MAPPING - EXACTLY matches old system (lab_manager/register/views/all_views.py lines 301-507)
        # Old system stores checkbox.text() DIRECTLY - no parsing, no transformation
        
        # field1: Service type (CRITICAL - must match old system exactly with Thai text)
        if data.service_type == 'Infectious Waste':
            fields[0] = 'ขยะติดเชื้อ'
        elif data.service_type == 'Jewelry':
            fields[0] = 'อัญมณี'
        elif data.service_type == 'Cremation':
            fields[0] = 'เผาซาก'
        else:
            fields[0] = 'None'
        
        # CRITICAL: Fields 2-16 are ALWAYS read for ALL service types (cremation section)
        cremation_details = service_data.get('cremation_details', {})
        
        # field2: laboratory_request_incineration_checkBox.text() - DIRECT from checkbox
        fields[1] = cremation_details.get('incineration', '')
        
        # field3: weight_tissues_lineEdit_2.text() - DIRECT from line edit
        fields[2] = cremation_details.get('weight', '')
        
        # field4: laboratory_request_bone_checkBox.text() - DIRECT from checkbox
        fields[3] = cremation_details.get('bone_storage', '')
        
        # field5: laboratory_request_cremation_checkBox.text() - DIRECT from checkbox
        fields[4] = cremation_details.get('ceremony', '')
        
        # field6: laboratory_dateEdit.text() - DIRECT from date edit
        fields[5] = cremation_details.get('date', '')
        
        # field7: laboratory_timeEdit.text() - DIRECT from time edit
        fields[6] = cremation_details.get('time', '')
        
        # field8: laboratory_request_daimond_checkBox.text() - DIRECT from checkbox
        fields[7] = cremation_details.get('diamond', '')
        
        # field9: laboratory_carcass_fresh_checkBox.text() - DIRECT from checkbox
        fields[8] = cremation_details.get('carcass_fresh', '')
        
        # field10: laboratory_carcass_aytolysus_checkBox.text() - DIRECT from checkbox
        fields[9] = cremation_details.get('carcass_autolysis', '')
        
        # field11: laboratory_carcass_unknow_checkBox.text() - DIRECT from checkbox
        fields[10] = cremation_details.get('carcass_unknown', '')
        
        # field12: laboratory_carcass_other_lineEdit.text() - DIRECT from line edit
        fields[11] = cremation_details.get('carcass_other', '')
        
        # field13: laboratory_place_necropy_checkBox_2.text() - DIRECT from checkbox
        fields[12] = cremation_details.get('place_necropsy', '')
        
        # field14: laboratory_place_other1_lineEdit_2.text() - DIRECT from line edit
        fields[13] = cremation_details.get('place_other1', '')
        
        # field15: laboratory_place_other2_lineEdit_2.text() - DIRECT from line edit
        fields[14] = cremation_details.get('place_other2', '')
        
        # field16: note_textEdit.toPlainText() - DIRECT from text edit
        fields[15] = cremation_details.get('note', '')
        
        # INFECTIOUS WASTE FIELDS (field17-32)
        # Old system stores checkbox.text() DIRECTLY in field17, 20, 23, then qty/weight separately
        if data.service_type == 'Infectious Waste':
            waste_details = service_data.get('waste_details', {})
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
            
            # Parse items - format: "checkbox.text(): qty qty weight kg"
            for item in items:
                if 'Tissues' in item:
                    parts = item.split(':', 1)
                    tissues_text = parts[0].strip()  # Store checkbox.text() DIRECTLY
                    if len(parts) > 1:
                        details = parts[1].strip()
                        if 'qty' in details:
                            tissues_qty = details.split('qty')[0].strip()
                        if 'kg' in details:
                            weight_part = details.split('kg')[0]
                            if 'qty' in weight_part:
                                weight_part = weight_part.split('qty')[1]
                            tissues_weight = weight_part.strip()
                            
                elif 'Needle' in item:
                    parts = item.split(':', 1)
                    needle_text = parts[0].strip()  # Store checkbox.text() DIRECTLY
                    if len(parts) > 1:
                        details = parts[1].strip()
                        if 'qty' in details:
                            needle_qty = details.split('qty')[0].strip()
                        if 'kg' in details:
                            weight_part = details.split('kg')[0]
                            if 'qty' in weight_part:
                                weight_part = weight_part.split('qty')[1]
                            needle_weight = weight_part.strip()
                            
                elif 'Syringe' in item:
                    parts = item.split(':', 1)
                    syringe_text = parts[0].strip()  # Store checkbox.text() DIRECTLY
                    if len(parts) > 1:
                        details = parts[1].strip()
                        if 'qty' in details:
                            syringe_qty = details.split('qty')[0].strip()
                        if 'kg' in details:
                            weight_part = details.split('kg')[0]
                            if 'qty' in weight_part:
                                weight_part = weight_part.split('qty')[1]
                            syringe_weight = weight_part.strip()
                else:
                    # Other items - store name DIRECTLY from line edit
                    if not other1_name:
                        parts = item.split(':', 1)
                        other1_name = parts[0].strip()
                        if len(parts) > 1:
                            details = parts[1].strip()
                            if 'qty' in details:
                                other1_qty = details.split('qty')[0].strip()
                            if 'kg' in details:
                                weight_part = details.split('kg')[0]
                                if 'qty' in weight_part:
                                    weight_part = weight_part.split('qty')[1]
                                other1_weight = weight_part.strip()
                    elif not other2_name:
                        parts = item.split(':', 1)
                        other2_name = parts[0].strip()
                        if len(parts) > 1:
                            details = parts[1].strip()
                            if 'qty' in details:
                                other2_qty = details.split('qty')[0].strip()
                            if 'kg' in details:
                                weight_part = details.split('kg')[0]
                                if 'qty' in weight_part:
                                    weight_part = weight_part.split('qty')[1]
                                other2_weight = weight_part.strip()
            
            # field17: infectioun_tissues_checkBox_2.text() - DIRECT checkbox text
            fields[16] = tissues_text
            
            # field18: number_pack_tissues_lineEdit.text()
            fields[17] = tissues_qty
            
            # field19: weight_tissues_lineEdit.text()
            fields[18] = tissues_weight
            
            # field20: infectioun_neddle_checkBox_2.text() - DIRECT checkbox text
            fields[19] = needle_text
            
            # field21: number_pack_needle_lineEdit.text()
            fields[20] = needle_qty
            
            # field22: weight_needle_lineEdit.text()
            fields[21] = needle_weight
            
            # field23: infectioun_syringe_checkBox_2.text() - DIRECT checkbox text
            fields[22] = syringe_text
            
            # field24: number_pack_syringe_lineEdit.text()
            fields[23] = syringe_qty
            
            # field25: weight_syringe_lineEdit.text()
            fields[24] = syringe_weight
            
            # field26: infectioun_other1_lineEdit_2.text() - DIRECT line edit text (user-entered name)
            fields[25] = other1_name
            
            # field27: number_pack_other1_lineEdit.text()
            fields[26] = other1_qty
            
            # field28: weight_other1_lineEdit.text()
            fields[27] = other1_weight
            
            # field29: infectioun_other2_lineEdit_2.text() - DIRECT line edit text (user-entered name)
            fields[28] = other2_name
            
            # field30: number_pack_other2_lineEdit.text()
            fields[29] = other2_qty
            
            # field31: weight_other2_lineEdit.text()
            fields[30] = other2_weight
            
            # field32: infectioun_remark_textEdit.toPlainText() - DIRECT text edit content
            fields[31] = waste_details.get('remark', '')
        
        # JEWELRY FIELDS (field33-69)
        # Old system stores checkbox.text() DIRECTLY for materials, sizes, shapes, jewelry types
        if data.service_type == 'Jewelry':
            jewelry_details = service_data.get('jewelry_details', {})
            
            material_str = jewelry_details.get('material', '')
            materials = [m.strip() for m in material_str.split(',')] if material_str else []
            
            # Initialize
            carcass_text = ''
            carcass_qty = ''
            carcass_weight = ''
            bone_text = ''
            bone_qty = ''
            bone_weight = ''
            hair_text = ''
            hair_qty = ''
            hair_weight = ''
            other1_text = ''
            other1_qty = ''
            other1_weight = ''
            other2_text = ''
            other2_qty = ''
            other2_weight = ''
            
            # Parse materials - format: "checkbox.text() (qty, weight kg)"
            for material in materials:
                if 'Carcass' in material:
                    if '(' in material:
                        carcass_text = material.split('(')[0].strip()  # Store checkbox.text() DIRECTLY
                        details = material.split('(')[1].rstrip(')')
                        parts = details.split(',')
                        if len(parts) >= 1:
                            carcass_qty = parts[0].strip()
                        if len(parts) >= 2:
                            carcass_weight = parts[1].replace('kg', '').strip()
                    else:
                        carcass_text = material
                        
                elif 'Bone' in material:
                    if '(' in material:
                        bone_text = material.split('(')[0].strip()  # Store checkbox.text() DIRECTLY
                        details = material.split('(')[1].rstrip(')')
                        parts = details.split(',')
                        if len(parts) >= 1:
                            bone_qty = parts[0].strip()
                        if len(parts) >= 2:
                            bone_weight = parts[1].replace('kg', '').strip()
                    else:
                        bone_text = material
                        
                elif 'Hair' in material or 'feather' in material:
                    if '(' in material:
                        hair_text = material.split('(')[0].strip()  # Store checkbox.text() DIRECTLY
                        details = material.split('(')[1].rstrip(')')
                        parts = details.split(',')
                        if len(parts) >= 1:
                            hair_qty = parts[0].strip()
                        if len(parts) >= 2:
                            hair_weight = parts[1].replace('kg', '').strip()
                    else:
                        hair_text = material
                else:
                    # Other materials - user-entered text from line edit
                    if not other1_text:
                        if '(' in material:
                            other1_text = material.split('(')[0].strip()
                            details = material.split('(')[1].rstrip(')')
                            parts = details.split(',')
                            if len(parts) >= 1:
                                other1_qty = parts[0].strip()
                            if len(parts) >= 2:
                                other1_weight = parts[1].replace('kg', '').strip()
                        else:
                            other1_text = material
                    elif not other2_text:
                        if '(' in material:
                            other2_text = material.split('(')[0].strip()
                            details = material.split('(')[1].rstrip(')')
                            parts = details.split(',')
                            if len(parts) >= 1:
                                other2_qty = parts[0].strip()
                            if len(parts) >= 2:
                                other2_weight = parts[1].replace('kg', '').strip()
                        else:
                            other2_text = material
            
            # field33: daimond_carcass_checkBox.text() - DIRECT checkbox text
            fields[32] = carcass_text
            
            # field34: daimond_number_carcass_lineEdit.text()
            fields[33] = carcass_qty
            
            # field35: daimond_weight_carcass_lineEdit.text()
            fields[34] = carcass_weight
            
            # field36: daimond_bone_checkBox.text() - DIRECT checkbox text
            fields[35] = bone_text
            
            # field37: daimond_number_bone_lineEdit.text()
            fields[36] = bone_qty
            
            # field38: daimond_weight_bone_lineEdit.text()
            fields[37] = bone_weight
            
            # field39: daimond_hair_checkBox.text() - DIRECT checkbox text
            fields[38] = hair_text
            
            # field40: daimond_number_hair_lineEdit.text()
            fields[39] = hair_qty
            
            # field41: daimond_weight_hair_lineEdit.text()
            fields[40] = hair_weight
            
            # field42: daimond_other1_lineEdit.text() - DIRECT line edit text (user-entered)
            fields[41] = other1_text
            
            # field43: daimond_number_other1_lineEdit.text()
            fields[42] = other1_qty
            
            # field44: daimond_weight_other1_lineEdit.text()
            fields[43] = other1_weight
            
            # field45: daimond_other2_lineEdit.text() - DIRECT line edit text (user-entered)
            fields[44] = other2_text
            
            # field46: daimond_number_other2_lineEdit.text()
            fields[45] = other2_qty
            
            # field47: daimond_weight_other2_lineEdit.text()
            fields[46] = other2_weight
            
            # Sizes (field48-53) - Store FULL checkbox.text() for each selected size
            size_str = jewelry_details.get('size', '')
            sizes = [s.strip() for s in size_str.split(',')] if size_str else []
            
            # field48: daimond_min_1carat_checkBox.text() - DIRECT if selected
            fields[47] = next((s for s in sizes if '<1 carat' in s), '')
            
            # field49: daimond_1carat_checkBox.text() - DIRECT if selected
            fields[48] = next((s for s in sizes if '1 carat' in s and '<1' not in s), '')
            
            # field50: daimond_2carat_checkBox.text() - DIRECT if selected
            fields[49] = next((s for s in sizes if '2 carat' in s), '')
            
            # field51: daimond_3carat_checkBox.text() - DIRECT if selected
            fields[50] = next((s for s in sizes if '3 carat' in s), '')
            
            # field52: daimond_4carat_checkBox.text() - DIRECT if selected
            fields[51] = next((s for s in sizes if '4 carat' in s), '')
            
            # field53: daimond_5carat_checkBox.text() - DIRECT if selected
            fields[52] = next((s for s in sizes if '5 carat' in s), '')
            
            # Shapes (field54-60) - Store FULL checkbox.text() for each selected shape
            shape_str = jewelry_details.get('shape', '')
            shapes = [s.strip() for s in shape_str.split(',')] if shape_str else []
            
            # field54: daimond_round_checkBox.text() - DIRECT if selected
            fields[53] = next((s for s in shapes if 'round' in s.lower()), '')
            
            # field55: daimond_oval_checkBox.text() - DIRECT if selected
            fields[54] = next((s for s in shapes if 'oval' in s.lower()), '')
            
            # field56: daimond_cushion_checkBox.text() - DIRECT if selected
            fields[55] = next((s for s in shapes if 'cushion' in s.lower()), '')
            
            # field57: daimond_princess_checkBox.text() - DIRECT if selected
            fields[56] = next((s for s in shapes if 'princess' in s.lower()), '')
            
            # field58: daimond_radiant_checkBox.text() - DIRECT if selected
            fields[57] = next((s for s in shapes if 'radiant' in s.lower()), '')
            
            # field59: daimond_marquise_checkBox.text() - DIRECT if selected
            fields[58] = next((s for s in shapes if 'marquise' in s.lower()), '')
            
            # field60: daimond_cutting_other_lineEdit.text() - User-entered custom shapes
            known_shapes = ['round', 'oval', 'cushion', 'princess', 'radiant', 'marquise']
            other_shapes = [s for s in shapes if not any(known in s.lower() for known in known_shapes)]
            fields[59] = ', '.join(other_shapes) if other_shapes else ''
            
            # Jewelry types (field61-66) - Store checkbox.text() and code separately
            jewelry_type_str = jewelry_details.get('jewelry_type', '')
            jewelry_types = [jt.strip() for jt in jewelry_type_str.split(',')] if jewelry_type_str else []
            
            # Ring
            ring_item = next((jt for jt in jewelry_types if 'ring' in jt.lower()), '')
            
            # field61: daimond_ring_checkBox.text() - DIRECT checkbox text (without code)
            if ring_item:
                fields[60] = ring_item.split('(Code:')[0].strip()
            else:
                fields[60] = ''
            
            # field62: daimond_code_ring_lineEdit.text() - Code only
            if ring_item and 'Code:' in ring_item:
                fields[61] = ring_item.split('Code:')[1].strip().rstrip(')')
            else:
                fields[61] = ''
            
            # Necklace
            necklace_item = next((jt for jt in jewelry_types if 'necklace' in jt.lower()), '')
            
            # field63: daimond_necklace_checkBox.text() - DIRECT checkbox text (without code)
            if necklace_item:
                fields[62] = necklace_item.split('(Code:')[0].strip()
            else:
                fields[62] = ''
            
            # field64: daimond_code_necklace_lineEdit.text() - Code only
            if necklace_item and 'Code:' in necklace_item:
                fields[63] = necklace_item.split('Code:')[1].strip().rstrip(')')
            else:
                fields[63] = ''
            
            # Earring
            earring_item = next((jt for jt in jewelry_types if 'earing' in jt.lower() or 'earring' in jt.lower()), '')
            
            # field65: daimond_earing_checkBox.text() - DIRECT checkbox text (without code)
            if earring_item:
                fields[64] = earring_item.split('(Code:')[0].strip()
            else:
                fields[64] = ''
            
            # field66: daimond_code_earing_lineEdit.text() - Code only
            if earring_item and 'Code:' in earring_item:
                fields[65] = earring_item.split('Code:')[1].strip().rstrip(')')
            else:
                fields[65] = ''
            
            # field67: daimond_color_textEdit.toPlainText() - DIRECT text edit content
            fields[66] = jewelry_details.get('color', '')
            
            # field68: daimond_price_textEdit.toPlainText() - DIRECT text edit content
            fields[67] = jewelry_details.get('price', '')
            
            # field69: daimond_remark_textEdit.toPlainText() - DIRECT text edit content
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