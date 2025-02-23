
        <TextField
            key={`field-${{oven}.id}-id`}
            margin="dense"
            name="id"
            value={formData.id}
            label="Id"
            type="number"
            fullWidth
            variant="outlined"
            required
            
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-name`}
            margin="dense"
            name="name"
            value={formData.name}
            label="Name"
            type="text"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: 450 }}
        />
    

        <TextField
            key={`field-${{oven}.id}-max_temp_positive`}
            margin="dense"
            name="max_temp_positive"
            value={formData.max_temp_positive}
            label="Max_temp_positive"
            type="text"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-max_temp_negative`}
            margin="dense"
            name="max_temp_negative"
            value={formData.max_temp_negative}
            label="Max_temp_negative"
            type="text"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-location`}
            margin="dense"
            name="location"
            value={formData.location}
            label="Location"
            type="text"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: 450 }}
        />
    

        <TextField
            key={`field-${{oven}.id}-power`}
            margin="dense"
            name="power"
            value={formData.power}
            label="Power"
            type="number"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-thermometer_type`}
            margin="dense"
            name="thermometer_type"
            value={formData.thermometer_type}
            label="Thermometer_type"
            type="text"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: 20 }}
        />
    

        <TextField
            key={`field-${{oven}.id}-thermometer_pin`}
            margin="dense"
            name="thermometer_pin"
            value={formData.thermometer_pin}
            label="Thermometer_pin"
            type="number"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-burner_pin`}
            margin="dense"
            name="burner_pin"
            value={formData.burner_pin}
            label="Burner_pin"
            type="number"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: undefined }}
        />
    

            <FormControl fullWidth margin="dense" variant="outlined">
                <InputLabel htmlFor="thermocouple_type">Thermocouple_type</InputLabel>
                <Select
                    key={`field-${{oven}.id}-thermocouple_type`}
                    native
                    value={formData.thermocouple_type || ''}
                    onChange={handleChange}
                    label="Thermocouple_type"
                    inputProps={
                        name: 'thermocouple_type',
                        id: 'thermocouple_type',
                    }
                >
                    <option aria-label="None" value="" />
                    <option value="MAX3155">MAX3155</option>
<option value="MAX3166">MAX3166</option>
<option value="DHT11">DHT11</option>
<option value="DHT22">DHT22</option>
                </Select>
            </FormControl>
        

        <TextField
            key={`field-${{oven}.id}-gpio_sensor_cs`}
            margin="dense"
            name="gpio_sensor_cs"
            value={formData.gpio_sensor_cs}
            label="Gpio_sensor_cs"
            type="number"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-gpio_sensor_clock`}
            margin="dense"
            name="gpio_sensor_clock"
            value={formData.gpio_sensor_clock}
            label="Gpio_sensor_clock"
            type="number"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-gpio_sensor_data`}
            margin="dense"
            name="gpio_sensor_data"
            value={formData.gpio_sensor_data}
            label="Gpio_sensor_data"
            type="number"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-gpio_sensor_di`}
            margin="dense"
            name="gpio_sensor_di"
            value={formData.gpio_sensor_di}
            label="Gpio_sensor_di"
            type="number"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-sensor_time_wait`}
            margin="dense"
            name="sensor_time_wait"
            value={formData.sensor_time_wait}
            label="Sensor_time_wait"
            type="number"
            fullWidth
            variant="outlined"
            
            defaultValue="2"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-pid_kp`}
            margin="dense"
            name="pid_kp"
            value={formData.pid_kp}
            label="Pid_kp"
            type="number"
            fullWidth
            variant="outlined"
            
            defaultValue="25"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-pid_ki`}
            margin="dense"
            name="pid_ki"
            value={formData.pid_ki}
            label="Pid_ki"
            type="number"
            fullWidth
            variant="outlined"
            
            defaultValue="10"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-pid_kd`}
            margin="dense"
            name="pid_kd"
            value={formData.pid_kd}
            label="Pid_kd"
            type="number"
            fullWidth
            variant="outlined"
            
            defaultValue="200"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-temp_scale`}
            margin="dense"
            name="temp_scale"
            value={formData.temp_scale}
            label="Temp_scale"
            type="text"
            fullWidth
            variant="outlined"
            
            defaultValue="'c'"
            inputProps={{ maxLength: 1 }}
        />
    

        <TextField
            key={`field-${{oven}.id}-emergency_shutoff_temp`}
            margin="dense"
            name="emergency_shutoff_temp"
            value={formData.emergency_shutoff_temp}
            label="Emergency_shutoff_temp"
            type="number"
            fullWidth
            variant="outlined"
            
            defaultValue="1500"
            inputProps={{ maxLength: undefined }}
        />
    

            <FormControlLabel
                key={`field-${{oven}.id}-kiln_must_catch_up`}
                name="kiln_must_catch_up"
                control={<Checkbox name={oven.kiln_must_catch_up} color="primary" defaultChecked />}
                label="Kiln_must_catch_up"
            />
        

        <TextField
            key={`field-${{oven}.id}-pid_control_window`}
            margin="dense"
            name="pid_control_window"
            value={formData.pid_control_window}
            label="Pid_control_window"
            type="number"
            fullWidth
            variant="outlined"
            
            defaultValue="5"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-thermocouple_offset`}
            margin="dense"
            name="thermocouple_offset"
            value={formData.thermocouple_offset}
            label="Thermocouple_offset"
            type="number"
            fullWidth
            variant="outlined"
            
            defaultValue="0"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-temperature_average_samples`}
            margin="dense"
            name="temperature_average_samples"
            value={formData.temperature_average_samples}
            label="Temperature_average_samples"
            type="number"
            fullWidth
            variant="outlined"
            
            defaultValue="40"
            inputProps={{ maxLength: undefined }}
        />
    

            <FormControlLabel
                key={`field-${{oven}.id}-ac_freq_50hz`}
                name="ac_freq_50hz"
                control={<Checkbox name={oven.ac_freq_50hz} color="primary"  />}
                label="Ac_freq_50hz"
            />
        

            <FormControlLabel
                key={`field-${{oven}.id}-automatic_restarts`}
                name="automatic_restarts"
                control={<Checkbox name={oven.automatic_restarts} color="primary" defaultChecked />}
                label="Automatic_restarts"
            />
        

        <TextField
            key={`field-${{oven}.id}-automatic_restart_window`}
            margin="dense"
            name="automatic_restart_window"
            value={formData.automatic_restart_window}
            label="Automatic_restart_window"
            type="number"
            fullWidth
            variant="outlined"
            
            defaultValue="15"
            inputProps={{ maxLength: undefined }}
        />
    

            <FormControlLabel
                key={`field-${{oven}.id}-simulate`}
                name="simulate"
                control={<Checkbox name={oven.simulate} color="primary"  />}
                label="Simulate"
            />
        

        <TextField
            key={`field-${{oven}.id}-sim_t_env`}
            margin="dense"
            name="sim_t_env"
            value={formData.sim_t_env}
            label="Sim_t_env"
            type="text"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-sim_c_heat`}
            margin="dense"
            name="sim_c_heat"
            value={formData.sim_c_heat}
            label="Sim_c_heat"
            type="text"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-sim_c_oven`}
            margin="dense"
            name="sim_c_oven"
            value={formData.sim_c_oven}
            label="Sim_c_oven"
            type="text"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-sim_p_heat`}
            margin="dense"
            name="sim_p_heat"
            value={formData.sim_p_heat}
            label="Sim_p_heat"
            type="text"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-sim_R_o_nocool`}
            margin="dense"
            name="sim_R_o_nocool"
            value={formData.sim_R_o_nocool}
            label="Sim_r_o_nocool"
            type="text"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-sim_R_o_cool`}
            margin="dense"
            name="sim_R_o_cool"
            value={formData.sim_R_o_cool}
            label="Sim_r_o_cool"
            type="text"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-sim_R_ho_noair`}
            margin="dense"
            name="sim_R_ho_noair"
            value={formData.sim_R_ho_noair}
            label="Sim_r_ho_noair"
            type="text"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-sim_R_ho_air`}
            margin="dense"
            name="sim_R_ho_air"
            value={formData.sim_R_ho_air}
            label="Sim_r_ho_air"
            type="text"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-kwh_rate`}
            margin="dense"
            name="kwh_rate"
            value={formData.kwh_rate}
            label="Kwh_rate"
            type="text"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: undefined }}
        />
    

        <TextField
            key={`field-${{oven}.id}-currency_type`}
            margin="dense"
            name="currency_type"
            value={formData.currency_type}
            label="Currency_type"
            type="text"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: 45 }}
        />
    

        <TextField
            key={`field-${{oven}.id}-kw_elements`}
            margin="dense"
            name="kw_elements"
            value={formData.kw_elements}
            label="Kw_elements"
            type="text"
            fullWidth
            variant="outlined"
            
            defaultValue="NULL"
            inputProps={{ maxLength: undefined }}
        />
    