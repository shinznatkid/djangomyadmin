var row_no = 0;
    
function addRows(num_rows){
    var collations = $('#collations_elem').html();
    console.log(collations);
    var row = '<tr>\
                    <td><input class="form-control" type="textbox" name="field_name[#]"></td>\
                    <td>\
                        <select class="form-control" name="field_type[#]">\
                            <option title="A 4-byte integer, signed range is -2,147,483,648 to 2,147,483,647, unsigned range is 0 to 4,294,967,295">INT</option>\
                            <option title="A variable-length (0-65,535) string, the effective maximum length is subject to the maximum row size">VARCHAR</option>\
                            <option title="A TEXT column with a maximum length of 65,535 (2^16 - 1) characters, stored with a two-byte prefix indicating the length of the value in bytes">TEXT</option>\
                            <option title="A date, supported range is 1000-01-01 to 9999-12-31">DATE</option>\
                            <optgroup label="Numeric">\
                                <option title="A 1-byte integer, signed range is -128 to 127, unsigned range is 0 to 255">TINYINT</option>\
                                <option title="A 2-byte integer, signed range is -32,768 to 32,767, unsigned range is 0 to 65,535">SMALLINT</option>\
                                <option title="A 3-byte integer, signed range is -8,388,608 to 8,388,607, unsigned range is 0 to 16,777,215">MEDIUMINT</option>\
                                <option title="A 4-byte integer, signed range is -2,147,483,648 to 2,147,483,647, unsigned range is 0 to 4,294,967,295">INT</option>\
                                <option title="An 8-byte integer, signed range is -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807, unsigned range is 0 to 18,446,744,073,709,551,615">BIGINT</option>\
                                <option disabled="disabled">-</option>\
                                <option title="A fixed-point number (M, D) - the maximum number of digits (M) is 65 (default 10), the maximum number of decimals (D) is 30 (default 0)">DECIMAL</option>\
                                <option title="A small floating-point number, allowable values are -3.402823466E+38 to -1.175494351E-38, 0, and 1.175494351E-38 to 3.402823466E+38">FLOAT</option>\
                                <option title="A double-precision floating-point number, allowable values are -1.7976931348623157E+308 to -2.2250738585072014E-308, 0, and 2.2250738585072014E-308 to 1.7976931348623157E+308">DOUBLE</option>\
                                <option title="Synonym for DOUBLE (exception: in REAL_AS_FLOAT SQL mode it is a synonym for FLOAT)">REAL</option>\
                                <option disabled="disabled">-</option>\
                                <option title="A bit-field type (M), storing M of bits per value (default is 1, maximum is 64)">BIT</option>\
                                <option title="A synonym for TINYINT(1), a value of zero is considered false, nonzero values are considered true">BOOLEAN</option>\
                                <option title="An alias for BIGINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE">SERIAL</option>\
                            </optgroup>\
                            <optgroup label="Date and time">\
                                <option title="A date, supported range is 1000-01-01 to 9999-12-31">DATE</option>\
                                <option title="A date and time combination, supported range is 1000-01-01 00:00:00 to 9999-12-31 23:59:59">DATETIME</option>\
                                <option title="A timestamp, range is 1970-01-01 00:00:01 UTC to 2038-01-09 03:14:07 UTC, stored as the number of seconds since the epoch (1970-01-01 00:00:00 UTC)">TIMESTAMP</option>\
                                <option title="A time, range is -838:59:59 to 838:59:59">TIME</option>\
                                <option title="A year in four-digit (4, default) or two-digit (2) format, the allowable values are 70 (1970) to 69 (2069) or 1901 to 2155 and 0000">YEAR</option>\
                            </optgroup>\
                            <optgroup label="String">\
                                <option title="A fixed-length (0-255, default 1) string that is always right-padded with spaces to the specified length when stored">CHAR</option>\
                                <option title="A variable-length (0-65,535) string, the effective maximum length is subject to the maximum row size">VARCHAR</option>\
                                <option disabled="disabled">-</option>\
                                <option title="A TEXT column with a maximum length of 255 (2^8 - 1) characters, stored with a one-byte prefix indicating the length of the value in bytes">TINYTEXT</option>\
                                <option title="A TEXT column with a maximum length of 65,535 (2^16 - 1) characters, stored with a two-byte prefix indicating the length of the value in bytes">TEXT</option>\
                                <option title="A TEXT column with a maximum length of 16,777,215 (2^24 - 1) characters, stored with a three-byte prefix indicating the length of the value in bytes">MEDIUMTEXT</option>\
                                <option title="A TEXT column with a maximum length of 4,294,967,295 or 4GiB (2^32 - 1) characters, stored with a four-byte prefix indicating the length of the value in bytes">LONGTEXT</option>\
                                <option disabled="disabled">-</option>\
                                <option title="Similar to the CHAR type, but stores binary byte strings rather than non-binary character strings">BINARY</option>\
                                <option title="Similar to the VARCHAR type, but stores binary byte strings rather than non-binary character strings">VARBINARY</option>\
                                <option disabled="disabled">-</option>\
                                <option title="A BLOB column with a maximum length of 255 (2^8 - 1) bytes, stored with a one-byte prefix indicating the length of the value">TINYBLOB</option>\
                                <option title="A BLOB column with a maximum length of 16,777,215 (2^24 - 1) bytes, stored with a three-byte prefix indicating the length of the value">MEDIUMBLOB</option>\
                                <option title="A BLOB column with a maximum length of 65,535 (2^16 - 1) bytes, stored with a two-byte prefix indicating the length of the value">BLOB</option>\
                                <option title="A BLOB column with a maximum length of 4,294,967,295 or 4GiB (2^32 - 1) bytes, stored with a four-byte prefix indicating the length of the value">LONGBLOB</option>\
                                <option disabled="disabled">-</option>\
                                <option title="An enumeration, chosen from the list of up to 65,535 values or the special \'\' error value">ENUM</option>\
                                <option title="A single value chosen from a set of up to 64 members">SET</option>\
                            </optgroup>\
                            <optgroup label="Spatial">\
                                <option title="A type that can store a geometry of any type">GEOMETRY</option>\
                                <option title="A point in 2-dimensional space">POINT</option>\
                                <option title="A curve with linear interpolation between points">LINESTRING</option>\
                                <option title="A polygon">POLYGON</option>\
                                <option title="A collection of points">MULTIPOINT</option>\
                                <option title="A collection of curves with linear interpolation between points">MULTILINESTRING</option>\
                                <option title="A collection of polygons">MULTIPOLYGON</option>\
                                <option title="A collection of geometry objects of any type">GEOMETRYCOLLECTION</option>\
                            </optgroup>    \
                        </select>\
                    </td>\
                    <td><input type="textbox" class="form-control" name="field_length[#]"></td>\
                    <td>\
                        <select class="form-control select-default" name="field_default_type[#]" class="default_type">\
                            <option value="NONE">None</option>\
                            <option value="USER_DEFINED">As defined:</option>\
                            <option value="NULL">NULL</option>\
                            <option value="CURRENT_TIMESTAMP">CURRENT_TIMESTAMP</option>\
                        </select>\
                        <br>\
                        <input type="text" class="form-control" name="field_default_value[#]" size="12" value="" style="display: none; margin-top:10px;">\
                    </td>\
                    <td>'+
                    collations    
                    +'</td>\
                    <td>\
                        <select class="form-control" name="field_attribute[#]">\
                           <option value="" selected="selected"></option>\
                           <option value="BINARY">BINARY</option>\
                           <option value="UNSIGNED">UNSIGNED</option>\
                           <option value="UNSIGNED ZEROFILL">UNSIGNED ZEROFILL</option>\
                           <option value="on update CURRENT_TIMESTAMP">on update CURRENT_TIMESTAMP</option>\
                       </select>\
                    </td>\
                    <td style="text-align:center;"><input name="field_null[#]" type="checkbox" value="NULL"></td>\
                    <td>\
                        <select class="form-control" name="field_key[#]">\
                            <option value="">---</option>\
                            <option value="PRIMARY" title="Primary">PRIMARY</option>\
                            <option value="UNIQUE" title="Unique">UNIQUE</option>\
                            <option value="INDEX" title="Index">INDEX</option>\
                            <option value="FULLTEXT" title="Fulltext">FULLTEXT</option>\
                        </select>\
                    </td>\
                    <td style="text-align:center;"><input name="field_extra[#]" type="checkbox" value="AUTO_INCREMENT"></td>\
                    <td><input type="text" class="form-control" name="field_comments[#]" size="12" value="" class="textfield"></td>\
                </tr>';        
    for(var i=0; i<num_rows; i++){
        var new_row = row.replace(/#/g, row_no);           
        $('#tb_table').append(new_row);    
        row_no++;
    }
    $('input[name="columns_num"]').val(row_no);
    bindDefaultType();
}

function bindDefaultType(){
    $('select[name^="field_default_type"]').change(function(){            
        if($(this).val() == 'USER_DEFINED'){
            $(this).parent().find('input[name^="field_default_value"]').show();                
        }
        else{
            $(this).parent().find('input[name^="field_default_value"]').hide();    
        }                
    });

    $('select[name^="field_default_type"]').change(function(){
        if($(this).val() == 'NULL'){
            $(this).parent().parent().find('input[name^="field_null"]').prop('checked', true);
        }
    });
    
    $('input[name^="field_null"]').change(function(){
        var default_type = $(this).parent().parent().find('select[name^="field_default_type"]');
        if($(this).is(':checked') == false && default_type.val() == 'NULL'){
            default_type.val('NONE');
        }
    });

}

function validate(){
    var error_msg = '';
    var reserved_words = [
        'ACCESSIBLE',
        'ADD',
        'ALL',
        'ALTER',
        'ANALYZE',
        'AND',
        'AS',
        'ASC',
        'ASENSITIVE',
        'BEFORE',
        'BETWEEN',
        'BIGINT',
        'BINARY',
        'BLOB',
        'BOTH',
        'BY',
        'CALL',
        'CASCADE',
        'CASE',
        'CHANGE',
        'CHAR',
        'CHARACTER',
        'CHECK',
        'COLLATE',
        'COLUMN',
        'CONDITION',
        'CONSTRAINT',
        'CONTINUE',
        'CONVERT',
        'CREATE',
        'CROSS',
        'CURRENT_DATE',
        'CURRENT_TIME',
        'CURRENT_TIMESTAMP',
        'CURRENT_USER',
        'CURSOR',
        'DATABASE',
        'DATABASES',
        'DAY_HOUR',
        'DAY_MICROSECOND',
        'DAY_MINUTE',
        'DAY_SECOND',
        'DEC',
        'DECIMAL',
        'DECLARE',
        'DEFAULT',
        'DELAYED',
        'DELETE',
        'DESC',
        'DESCRIBE',
        'DETERMINISTIC',
        'DISTINCT',
        'DISTINCTROW',
        'DIV',
        'DOUBLE',
        'DROP',
        'DUAL',
        'EACH',
        'ELSE',
        'ELSEIF',
        'ENCLOSED',
        'ESCAPED',
        'EXISTS',
        'EXIT',
        'EXPLAIN',
        'FALSE',
        'FETCH',
        'FLOAT',
        'FLOAT4',
        'FLOAT8',
        'FOR',
        'FORCE',
        'FOREIGN',
        'FROM',
        'FULLTEXT',
        'GRANT',
        'GROUP',
        'HAVING',
        'HIGH_PRIORITY',
        'HOUR_MICROSECOND',
        'HOUR_MINUTE',
        'HOUR_SECOND',
        'IF',
        'IGNORE',
        'IN',
        'INDEX',
        'INFILE',
        'INNER',
        'INOUT',
        'INSENSITIVE',
        'INSERT',
        'INT',
        'INT1',
        'INT2',
        'INT3',
        'INT4',
        'INT8',
        'INTEGER',
        'INTERVAL',
        'INTO',
        'IS',
        'ITERATE',
        'JOIN',
        'KEY',
        'KEYS',
        'KILL',
        'LEADING',
        'LEAVE',
        'LEFT',
        'LIKE',
        'LIMIT',
        'LINEAR',
        'LINES',
        'LOAD',
        'LOCALTIME',
        'LOCALTIMESTAMP',
        'LOCK',
        'LONG',
        'LONGBLOB',
        'LONGTEXT',
        'LOOP',
        'LOW_PRIORITY',
        'MASTER_SSL_VERIFY_SERVER_CERT',
        'MATCH',
        'MAXVALUE',
        'MEDIUMBLOB',
        'MEDIUMINT',
        'MEDIUMTEXT',
        'MIDDLEINT',
        'MINUTE_MICROSECOND',
        'MINUTE_SECOND',
        'MOD',
        'MODIFIES',
        'NATURAL',
        'NOT',
        'NO_WRITE_TO_BINLOG',
        'NULL',
        'NUMERIC',
        'ON',
        'OPTIMIZE',
        'OPTION',
        'OPTIONALLY',
        'OR',
        'ORDER',
        'OUT',
        'OUTER',
        'OUTFILE',
        'PRECISION',
        'PRIMARY',
        'PROCEDURE',
        'PURGE',
        'RANGE',
        'READ',
        'READS',
        'READ_WRITE',
        'REAL',
        'REFERENCES',
        'REGEXP',
        'RELEASE',
        'RENAME',
        'REPEAT',
        'REPLACE',
        'REQUIRE',
        'RESIGNAL',
        'RESTRICT',
        'RETURN',
        'REVOKE',
        'RIGHT',
        'RLIKE',
        'SCHEMA',
        'SCHEMAS',
        'SECOND_MICROSECOND',
        'SELECT',
        'SENSITIVE',
        'SEPARATOR',
        'SET',
        'SHOW',
        'SIGNAL',
        'SMALLINT',
        'SPATIAL',
        'SPECIFIC',
        'SQL',
        'SQLEXCEPTION',
        'SQLSTATE',
        'SQLWARNING',
        'SQL_BIG_RESULT',
        'SQL_CALC_FOUND_ROWS',
        'SQL_SMALL_RESULT',
        'SSL',
        'STARTING',
        'STRAIGHT_JOIN',
        'TABLE',
        'TERMINATED',
        'THEN',
        'TINYBLOB',
        'TINYINT',
        'TINYTEXT',
        'TO',
        'TRAILING',
        'TRIGGER',
        'TRUE',
        'UNDO',
        'UNION',
        'UNIQUE',
        'UNLOCK',
        'UNSIGNED',
        'UPDATE',
        'USAGE',
        'USE',
        'USING',
        'UTC_DATE',
        'UTC_TIME',
        'UTC_TIMESTAMP',
        'VALUES',
        'VARBINARY',
        'VARCHAR',
        'VARCHARACTER',
        'VARYING',
        'WHEN',
        'WHERE',
        'WHILE',
        'WITH',
        'WRITE',
        'XOR',
        'YEAR_MONTH',
        'ZEROFILL',
        'GENERAL',
        'IGNORE_SERVER_IDS',
        'MASTER_HEARTBEAT_PERIOD',
        'MAXVALUE',
        'RESIGNAL',
        'SIGNAL',
        'SLOW'
    ];
    $('input[name^="field_name"]').each(function(index){
        var name = $(this).val();        
        
        if(name){

            if($.inArray(name.toUpperCase(), reserved_words) != -1){
                error_msg = name + ' is a reserved_word';                
                return;
            }   

            var tr = $(this).parent().parent();
            var type = tr.find('select[name^="field_type"]').val();

            if(type.match('^VAR')){                
                var length = tr.find('input[name^="field_length"]').val();
                if(!length){
                    error_msg = name + ' must be specified length of ' + type;                    
                    return;
                }
                else if(length <= 0){
                    error_msg = name + ' must have length more than 0';                    
                    return; 
                }
            }                
            else if(type=='ENUM' || type=='SET'){
                var length = tr.find('input[name^="field_length"]').val();
                values = length.split(',')
                for(var i=0; i<values.length; i++){
                    var valid_value = values[i].match('^\'[a-zA-Z0-9\-]+\'$') || values[i].match('^\"[a-zA-Z0-9\-]+\"$') || values[i].match('[0-9\-]+')
                    if(!valid_value){
                        error_msg = 'Invalid values (' + length + ') for ' + type;                
                        return;              
                    }
                }
            }

            var default_value = tr.find('select[name^="field_default_type"]').val();                
            if(default_value == 'CURRENT_TIMESTAMP' && type != 'TIMESTAMP'){
                error_msg = 'Invalid default value (' + default_value + ') for ' + type;                
                return;    
            }

            
            var attribute = tr.find('select[name^="field_attribute"]').val();
            if(attribute.match('CURRENT_TIMESTAMP$') && type != 'TIMESTAMP'){
                error_msg = 'Invalid attribute (' + attribute + ') for ' + type;
                return;    
            }               
            else if(attribute == 'BINARY' && !(type.match('CHAR$') || type.match('TEXT$'))){
                error_msg = 'Invalid attribute (' + attribute + ') for ' + type;                
                return;    
            }
            else if(attribute.match('^UNSIGNED') && !(type.match('INT') || $.inArray(type, ['REAL', 'DOUBLE', 'FLOAT', 'DECIMAL', 'NUMERIC']) != -1)){
                error_msg = 'Invalid attribute (' + attribute + ') for ' + type;                
                return;    
            }
        }
    });     
    
    return error_msg;      
}
