/**
 * 
 */
package cern.accsoft.steering.jmad.modeldefs.defs.tt10sps;

import cern.accsoft.steering.jmad.domain.file.CallableModelFileImpl;
import cern.accsoft.steering.jmad.domain.file.ModelFile;
import cern.accsoft.steering.jmad.domain.file.ModelPathOffsetsImpl;
import cern.accsoft.steering.jmad.domain.file.CallableModelFile.ParseType;
import cern.accsoft.steering.jmad.domain.file.ModelFile.ModelFileLocation;
import cern.accsoft.steering.jmad.domain.machine.MadxRange;
import cern.accsoft.steering.jmad.domain.machine.RangeDefinitionImpl;
import cern.accsoft.steering.jmad.domain.machine.SequenceDefinitionImpl;
import cern.accsoft.steering.jmad.domain.machine.filter.RegexNameFilter;
import cern.accsoft.steering.jmad.domain.result.tfs.TfsResult;
import cern.accsoft.steering.jmad.domain.twiss.TwissInitialConditionsImpl;
import cern.accsoft.steering.jmad.domain.types.enums.JMadPlane;
import cern.accsoft.steering.jmad.factory.BeamFactory;
import cern.accsoft.steering.jmad.modeldefs.ModelDefinitionFactory;
import cern.accsoft.steering.jmad.modeldefs.domain.JMadModelDefinition;
import cern.accsoft.steering.jmad.modeldefs.domain.JMadModelDefinitionImpl;
import cern.accsoft.steering.jmad.modeldefs.domain.OpticsDefinition;
import cern.accsoft.steering.jmad.modeldefs.domain.OpticsDefinitionImpl;

/**
 * This class is the actual model configuration for the TT2TT10SPS transfer line for Ions.
 * 
 * @author F.M. Velotti copied from Kajetan Fuchsberger implementation
 */
public class TT10spsIonsModelDefinitionFactory implements ModelDefinitionFactory {

    @Override
    public JMadModelDefinition create() {
        JMadModelDefinitionImpl modelDefinition = new JMadModelDefinitionImpl();
        modelDefinition.setName("PB81TT10SPS");

        ModelPathOffsetsImpl offsets = new ModelPathOffsetsImpl();
        offsets.setResourceOffset("tt10sps/2016");
        modelDefinition.setModelPathOffsets(offsets);

        modelDefinition.addInitFile(new CallableModelFileImpl("beam/lhc_beam_inj.madx", ModelFileLocation.RESOURCE));
        modelDefinition.addInitFile(new CallableModelFileImpl("sequence/tt10spsPb.seq", ModelFileLocation.RESOURCE));

        /*
         * OPTICS
         */
        String[] strengthFileNames = new String[] { 
                "str/tt10_sps_pb80-2018.str",
                "str/tt10_sps_pb81-2018.str"
               };
        

        for (String strengthFileName : strengthFileNames) {
            String opticsName = strengthFileName.replaceAll("str/tt10_sps_", "SPSInjection-").replaceAll(".str", "");
            OpticsDefinition opticsDefinition = new OpticsDefinitionImpl(opticsName,
                    new ModelFile[] { new CallableModelFileImpl(strengthFileName, ModelFileLocation.RESOURCE,
                            ParseType.STRENGTHS) });
            modelDefinition.addOpticsDefinition(opticsDefinition);
        }
        modelDefinition.setDefaultOpticsDefinition(modelDefinition.getOpticsDefinitions().get(0));

        /*
         * SEQUENCE
         * This works for JMAD but not for the optics uploader...
         * MadxRange range = new MadxRange("strn", "#e");
         */

       
        SequenceDefinitionImpl tt10sps = new SequenceDefinitionImpl("pbtt10sps",null);
        modelDefinition.setDefaultSequenceDefinition(tt10sps);
        
        
        RangeDefinitionImpl tt10spsrange = new RangeDefinitionImpl(tt10sps, "ALL", createTT10InitialConditions());
        tt10sps.setDefaultRangeDefinition(tt10spsrange);

        return modelDefinition;
    }

    /**
     * Twiss initial conditions for transferline TT2 after strn1
     */
    private final TwissInitialConditionsImpl createTT10InitialConditions() {
        TwissInitialConditionsImpl twissInitialConditions = new TwissInitialConditionsImpl("tt10sps-twiss");

        /** initial twiss parameters at STRN for TT2 @ 26 GeV/c for lead ions
        (the beam line starts at the stripper STRN)
        Twiss parameters change at STRN due to multiple scattering (10/10/2007)

        BETX0  :=  4.76923;
        ALFX0  :=  0.0;
        MUX0   :=  0.000000000000;
        BETY0  :=  4.71875;
        ALFY0  :=  0.0;
        MUY0   :=  0.000000000000;
        X0     :=  0.000000000000;
        PX0    :=  0.000000000000;
        Y0     :=  0.000000000000;
        PY0    :=  0.000000000000;
        T0     :=  0.000000000000;
        PT0    :=  0.000000000000;
        DX0    :=  0.0;
        DPX0   :=  0.213;
        DY0    :=  0.0;
        DPY0   := -0.019;
        ***/

        twissInitialConditions.setDeltap(0.0);
        twissInitialConditions.setBetx(4.76923);
        twissInitialConditions.setAlfx(0.0);
        twissInitialConditions.setDx(0.0);
        twissInitialConditions.setDpx(0.213);
        twissInitialConditions.setBety(4.71875);
        twissInitialConditions.setAlfy(0.0);
        twissInitialConditions.setDy(0.0);
        twissInitialConditions.setDpy(-0.019);
        twissInitialConditions.setCalcAtCenter(true);
        twissInitialConditions.setClosedOrbit(false);
        return twissInitialConditions;

    }

}
