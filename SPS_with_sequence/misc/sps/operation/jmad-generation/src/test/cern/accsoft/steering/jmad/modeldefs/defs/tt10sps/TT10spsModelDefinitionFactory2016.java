/**
 * 
 */
package cern.accsoft.steering.jmad.modeldefs.defs.tt10sps;

import cern.accsoft.steering.jmad.domain.file.CallableModelFileImpl;
import cern.accsoft.steering.jmad.domain.file.ModelFile;
import cern.accsoft.steering.jmad.domain.file.ModelPathOffsetsImpl;
import cern.accsoft.steering.jmad.domain.file.CallableModelFile.ParseType;
import cern.accsoft.steering.jmad.domain.file.ModelFile.ModelFileLocation;
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
 * This class is the actual model configuration for the TT2TT10 transfer line.
 * 
 * @author Kajetan Fuchsberger (kajetan.fuchsberger at cern.ch)
 */
public class TT10spsModelDefinitionFactory2016 implements ModelDefinitionFactory {

    @Override
    public JMadModelDefinition create() {
        JMadModelDefinitionImpl modelDefinition = new JMadModelDefinitionImpl();
        modelDefinition.setName("TT10SPS");

        ModelPathOffsetsImpl offsets = new ModelPathOffsetsImpl();
        offsets.setResourceOffset("tt10sps/2016");
        modelDefinition.setModelPathOffsets(offsets);

        modelDefinition.addInitFile(new CallableModelFileImpl("beam/lhc_beam_inj.madx", ModelFileLocation.RESOURCE));
        modelDefinition.addInitFile(new CallableModelFileImpl("sequence/tt10sps.seq", ModelFileLocation.RESOURCE));

        /*
         * OPTICS
         */
        String[] strengthFileNames = new String[] {
                "str/tt10_sps_Q22-2016v1.str"
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
         */

       
        SequenceDefinitionImpl tt10sps = new SequenceDefinitionImpl("tt2tt10sps",null);
        modelDefinition.setDefaultSequenceDefinition(tt10sps);
        RangeDefinitionImpl tt10spsrange = new RangeDefinitionImpl(tt10sps, "ALL", createTT10InitialConditions());
        tt10sps.setDefaultRangeDefinition(tt10spsrange);

        return modelDefinition;
    }

    /**
     * Twiss initial conditions for transferline TT2TT10
     */
    private final TwissInitialConditionsImpl createTT10InitialConditions() {
        TwissInitialConditionsImpl twissInitialConditions = new TwissInitialConditionsImpl("tt10sps-twiss");

       
        twissInitialConditions.setDeltap(0.0);
        twissInitialConditions.setBetx(26.1431);
        twissInitialConditions.setAlfx(-2.2287);
        twissInitialConditions.setDx(3.0414);
        twissInitialConditions.setDpx(0.25256);
        twissInitialConditions.setBety(10.883);
        twissInitialConditions.setAlfy(0.762);
        twissInitialConditions.setDy(0.024);
        twissInitialConditions.setDpy(-0.014);
        twissInitialConditions.setCalcAtCenter(true);
        twissInitialConditions.setClosedOrbit(false);
        return twissInitialConditions;

    }

}
